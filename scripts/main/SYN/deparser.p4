/*-----------------Deparser-----------------*/
control MyDeparser(
    packet_out packet,
    inout    headers hdr,
    in    metadata meta,
    in    pna_main_output_metadata_t ostd)
{
    apply {
        
        /*Emit the Ethernet Header below*/
        packet.emit(hdr.ethernet);
        /*Emit the IPv4 Header below*/
        packet.emit(hdr.ipv4);
        /*Emit the TCP Header below*/
        packet.emit(hdr.tcp);
    
    }
}
