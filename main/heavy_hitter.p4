control HEAVYHitter(
    inout headers_t       hdr,
    inout main_metadata_t meta)
{   
    Hash<bit<16>> (PNA_HashAlgorithm_t.CRC16) h0;
    
    action hf0() {
       meta.flow_id0 = h0.get_hash((bit<16>)0, {hdr.tcp.srcPort,hdr.tcp.dstPort,hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, (bit<16>)32768);
    } 
    
    action hf1() {
        meta.flow_id1 = h0.get_hash((bit<16>)100, {hdr.tcp.srcPort,hdr.tcp.dstPort,hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, (bit<16>)32768);   
    }
    
    action hf2() {
        meta.flow_id2 = h0.get_hash((bit<16>)200, {hdr.tcp.srcPort,hdr.tcp.dstPort,hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, (bit<16>)32768);
    }
    
    action hf3() {
        meta.flow_id3 = h0.get_hash((bit<16>)300, {hdr.tcp.srcPort,hdr.tcp.dstPort,hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, (bit<16>)32768);
    }

    Register<bit<20>, bit<16>>(32768) ht0;
    Register<bit<20>, bit<16>>(32768) ht1;
    Register<bit<20>, bit<16>>(32768) ht2;
    Register<bit<20>, bit<16>>(32768) ht3;

    apply {
        meta.attack = 5;

        meta.minimum = 1048575;
        hf0();
        hf1();
        hf2();
        hf3();

        meta.count_0 = ht0.read(meta.flow_id0);
        meta.count_1 = ht1.read(meta.flow_id1);
        meta.count_2 = ht2.read(meta.flow_id2);
        meta.count_3 = ht3.read(meta.flow_id3);

        meta.dif = meta.minimum - meta.count_0;
        if(meta.dif > 0){
            meta.minimum = meta.count_0;
        }

        meta.dif = meta.minimum - meta.count_1;
        if(meta.dif > 0){
            meta.minimum = meta.count_1;
        }

        meta.dif = meta.minimum - meta.count_2;
        if(meta.dif > 0){
            meta.minimum = meta.count_2;
        }

        meta.dif = meta.minimum - meta.count_3;
        if(meta.dif > 0){
            meta.minimum = meta.count_3;
        }
        
        if(meta.minimum > THRESH_HH){
            drop_packet();
        } 
        else {
            ht0.write(meta.flow_id0,meta.count_0+1);
            ht1.write(meta.flow_id1,meta.count_1+1);
            ht2.write(meta.flow_id2,meta.count_2+1);
            ht3.write(meta.flow_id3,meta.count_3+1);
        }

    }
}
