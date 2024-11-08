



struct ethernet_t {
	bit<48> dstAddr
	bit<48> srcAddr
	bit<16> etherType
}

struct ipv4_t {
	bit<8> version_ihl
	bit<8> diffserv
	bit<16> totalLen
	bit<16> identification
	bit<16> flags_fragOffset
	bit<8> ttl
	bit<8> protocol
	bit<16> hdrChecksum
	bit<32> srcAddr
	bit<32> dstAddr
}

struct tcp_t {
	bit<16> srcPort
	bit<16> dstPort
	bit<32> seqNo
	bit<32> ackNo
	bit<8> dataOffset_res
	bit<8> ecn_flags
	bit<16> window
	bit<16> checksum
	bit<16> urgentPtr
}

struct forward_arg_t {
	bit<32> port_id
}

struct metadata {
	bit<32> pna_main_input_metadata_input_port
	bit<32> local_metadata_drop_percent
	bit<32> local_metadata_syn_counts
	bit<32> local_metadata_percent_iterator
	bit<32> pna_main_output_metadata_output_port
	bit<8> MainControlT_tmp
	bit<8> MainControlT_tmp_0
}
metadata instanceof metadata

header ethernet instanceof ethernet_t
header ipv4 instanceof ipv4_t
header tcp instanceof tcp_t

regarray drop_percent_reg_0 size 0x1 initval 0
regarray syn_counts_reg_0 size 0x1 initval 0
regarray percent_iterator_reg_0 size 0x1 initval 0
regarray direction size 0x100 initval 0
action forward args instanceof forward_arg_t {
	mov m.pna_main_output_metadata_output_port t.port_id
	return
}

action drop args none {
	drop
	return
}

table forwarding {
	key {
		h.ipv4.dstAddr exact
	}
	actions {
		forward
		drop
	}
	default_action drop args none 
	size 0x400
}


apply {
	rx m.pna_main_input_metadata_input_port
	extract h.ethernet
	jmpeq MYPARSER_PARSE_IPV4 h.ethernet.etherType 0x800
	jmp MYPARSER_ACCEPT
	MYPARSER_PARSE_IPV4 :	extract h.ipv4
	jmpeq MYPARSER_PARSE_TCP h.ipv4.protocol 0x6
	jmp MYPARSER_ACCEPT
	MYPARSER_PARSE_TCP :	extract h.tcp
	MYPARSER_ACCEPT :	jmpnv LABEL_END h.ipv4
	table forwarding
	jmpnv LABEL_END h.tcp
	regrd m.local_metadata_drop_percent drop_percent_reg_0 0x0
	mov m.MainControlT_tmp h.tcp.ecn_flags
	and m.MainControlT_tmp 0x1F
	mov m.MainControlT_tmp_0 m.MainControlT_tmp
	and m.MainControlT_tmp_0 0x1F
	jmpneq LABEL_END m.MainControlT_tmp_0 0x2
	regrd m.local_metadata_syn_counts syn_counts_reg_0 0x0
	add m.local_metadata_syn_counts 0x1
	regwr syn_counts_reg_0 0x0 m.local_metadata_syn_counts
	jmpgt LABEL_TRUE_2 m.local_metadata_syn_counts 0x64
	jmp LABEL_END
	LABEL_TRUE_2 :	regrd m.local_metadata_percent_iterator percent_iterator_reg_0 0x0
	jmplt LABEL_TRUE_3 m.local_metadata_percent_iterator m.local_metadata_drop_percent
	jmplt LABEL_TRUE_4 m.local_metadata_percent_iterator 0x64
	jmpneq LABEL_END m.local_metadata_percent_iterator 0x64
	mov m.local_metadata_percent_iterator 0x0
	regwr percent_iterator_reg_0 0x0 m.local_metadata_percent_iterator
	jmp LABEL_END
	jmp LABEL_END
	LABEL_TRUE_4 :	add m.local_metadata_percent_iterator 0x1
	and m.local_metadata_percent_iterator 0x7F
	regwr percent_iterator_reg_0 0x0 m.local_metadata_percent_iterator
	jmp LABEL_END
	LABEL_TRUE_3 :	add m.local_metadata_percent_iterator 0x1
	and m.local_metadata_percent_iterator 0x7F
	regwr percent_iterator_reg_0 0x0 m.local_metadata_percent_iterator
	drop
	LABEL_END :	emit h.ethernet
	emit h.ipv4
	emit h.tcp
	tx m.pna_main_output_metadata_output_port
}


