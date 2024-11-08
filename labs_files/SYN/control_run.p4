/*-----------------Control-----------------*/
#define THRESH 1000000

control MainControl(
    inout headers hdr,
    inout metadata meta,
    in pna_main_input_metadata_t istd,
    inout pna_main_output_metadata_t ostd) {    

    Register<bit<7>, bit<1>>(1) drop_percent_reg;
    Register<bit<32>, bit<1>>(1) syn_counts_reg;
    Register<bit<7>, bit<1>>(1) percent_iterator_reg;

    action forward (EthernetAddress dstAddr, PortId_t port_id) {
        send_to_port(port_id);
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl -1;
    }
    action drop () {
        drop_packet();
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

    apply {

        if(hdr.ipv4.isValid()) {
            forwarding.apply();

             if(hdr.tcp.isValid()){
                meta.drop_percent = drop_percent_reg.read(0);

                if(hdr.tcp.flags == 2) {
                    meta.syn_counts = 0;

                    meta.syn_counts = syn_counts_reg.read(0);
                    meta.syn_counts = meta.syn_counts +1;
                    syn_counts_reg.write(0, meta.syn_counts);
                
                    if(meta.syn_counts > THRESH){
                        meta.percent_iterator = percent_iterator_reg.read(0);
                        
                        if(meta.percent_iterator < meta.drop_percent){
                            meta.percent_iterator = meta.percent_iterator + 1;
                            percent_iterator_reg.write(0, meta.percent_iterator);
                            drop();
                        }
                        else if (meta.percent_iterator < 100) {
                            meta.percent_iterator = meta.percent_iterator + 1;
                            percent_iterator_reg.write(0, meta.percent_iterator);
                        }
                        else if (meta.percent_iterator == 100) {
                            meta.percent_iterator = 0;
                            percent_iterator_reg.write(0, meta.percent_iterator);
                        }
                    }
                }
             }
        }
    }  
}
