/*-----------------Main-----------------*/
#include <core.p4>
#include <dpdk/pna.p4>

#include "parser.p4"
#include "precontrol.p4"
#include "control.p4"
#include "deparser.p4"

/*Insert the blocks below this comment*/
PNA_NIC(
MyParser(),
PreControl(),
MainControl(),
MyDeparser()
) main;
