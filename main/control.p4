
control MainControlImpl(
    inout headers_t       hdr,
    inout main_metadata_t meta,
    in    pna_main_input_metadata_t  istd,
    inout pna_main_output_metadata_t ostd)
{   

    action drop () {
        drop_packet();
    }

    action forward (EthernetAddress dstAddr, PortId_t port_id) {
        send_to_port(port_id);
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl -1;
    }

    action noAction () {
    }

    action add_miss () {
        if (meta.add == 1) {
            add_entry(action_name = "noAction", action_params = {}, expire_time_profile_id = EXPIRE_TIME_PROFILE_ID);
        }
        else {
            noAction();
        }
    }

    table forwarding {
        key = { 
            hdr.ipv4.dstAddr: exact; 
        }
        actions = { 
            forward;
            drop;
        }
        size = 1024;
        default_action = drop;
    }

    table open_tcp {
        key = {
            hdr.ipv4.srcAddr: exact;
        }
        actions = {
            noAction;
            add_miss;
        }
        add_on_miss = true;
        default_action = add_miss;
        size = 1024;
    }
     
    HEAVYHitter() heavy_hitter;
    SYNFlood() syn_flood;
    SYNACKFlood() syn_ack_flood;
    ACKFlood() ack_flood;
    FINFlood() fin_flood;
    ICMPFlood() icmp_flood;

    Register<bit<5>, bit<1>>(1) attack;

    Register<bit<5>, bit<1>>(1) test;

    apply {
        
        if(hdr.ipv4.isValid()) {
            forwarding.apply();
            meta.attack = 0;
            meta.test = (bit<5>)hdr.ipv4.protocol;
            test.write(0,meta.test);

            if(hdr.tcp.isValid()) {
                if(hdr.tcp.flags == 0x2) { // SYN 00010 , attack 1
                    syn_flood.apply(hdr, meta);
                }
                else if(hdr.tcp.flags == 0x12) { //SYN-ACK 10010 , attack 2
                    syn_ack_flood.apply(hdr, meta);
                }
                else if(hdr.tcp.flags == 0x10) { //ACK 10000 , attack 3
                    ack_flood.apply(hdr, meta);
                    open_tcp.apply();
                }
                else if(hdr.tcp.flags == 0x01 || hdr.tcp.flags == 0x04 || hdr.tcp.flags == 0x05) { 
                    //FIN 00001 RST 00100 FIN-RST 00101  , attack 4
                    fin_flood.apply(hdr, meta);  
                    if(open_tcp.apply().miss){drop();} 
                }
                else { // TCP FLAGS 00000 , attack 5
                    heavy_hitter.apply(hdr, meta);
                }
            }

            if (hdr.icmp.isValid()){ 
                if(hdr.icmp.type == 0x08 || hdr.icmp.type == 0x63) // REQ 0x8 or 0x63 , attack 6
                icmp_flood.apply(hdr, meta);
            }
        }
        attack.write(0,meta.attack);
    }
}