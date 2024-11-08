control ICMPFlood(
    inout headers_t       hdr,
    inout main_metadata_t meta)
{   

    Register<bit<8>, bit<1>>(1) test2;
    
    apply {
        meta.attack = 6;
        meta.test2 = hdr.icmp.type;
        test2.write(0,meta.test2); 
    }
}
