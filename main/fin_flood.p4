control FINFlood(
    inout headers_t       hdr,
    inout main_metadata_t meta)
{   

    apply {
        meta.attack = 4;
        meta.add = 0; 
    }
}
