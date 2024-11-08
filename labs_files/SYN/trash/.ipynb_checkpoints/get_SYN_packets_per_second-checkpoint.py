import telnetlib
import time

# Telnet server details
host = "0.0.0.0"
port = 8086
timeout = 1

# Command to send
reset = b"pipeline PIPELINE0 regwr syn_counts_reg_0 value 0 index 0\n"
command = b"pipeline PIPELINE0 stats\n"
# command = b"pipeline PIPELINE0 regrst syn_counts_reg_0 rst_index 1\n"

# Function to connect to telnet server and send command
def telnet_session(host, port, command, timeout):
    port1_packets_prev = 0
    port0_packets_prev = 0
    packets_dropped_prev = 0
    key = 0

    try:
        # Connect to the telnet server
        tn = telnetlib.Telnet(host, port, timeout)
        
        # Read until prompt or login message
        tn.read_until(b"Escape character is", timeout)
        
        # Send command
        # tn.write(command)
        
        # Continue reading output (optional)
        while True:
            tn.write(reset)
            print("reset register-------------------------")
            tn.write(command)
            output = tn.read_until(b"tables:\n", timeout)
            string_output = output.decode('utf-8')
            # print(string_output)
            port1_packets_curr = int(string_output.split("Port 1: packets ")[1].split(" bytes")[0])
            port0_packets_curr = int(string_output.split("Output ports:")[1].split("Port 0: packets ")[1].split(" bytes")[0])
            packets_dropped_curr = int(string_output.split("packets dropped ")[3].split(" bytes")[0])
            
            # drops = (port1_packets_curr-port1_packets_prev)-(port0_packets_curr-port0_packets_prev)

            # if drops < 0:
            #     drops = 0

            if key == 1:
                print("from h3",port1_packets_curr-port1_packets_prev,"to h1",port0_packets_curr-port0_packets_prev,"drops",packets_dropped_curr-packets_dropped_prev,"in the last sec")

            port1_packets_prev = port1_packets_curr
            port0_packets_prev = port0_packets_curr
            packets_dropped_prev = packets_dropped_curr

            key = 1
            time.sleep(1)  # Adjust as needed to control frequency of command sending
            print("-----------------------------------------------")
            
    except Exception as e:
        print(f"Error: {e}")

    finally:
        tn.close()

# Start the telnet session
telnet_session(host, port, command, timeout)

# full_output = "b'pipeline> Input ports:\n\tPort 0: packets 13 bytes 1754 empty 3754862366\n\tPort 1: packets 14 bytes 1852 empty 3754862386\n\nOutput ports:\n\tPort 0: packets 0 bytes 0 packets dropped 0 bytes dropped 0 clone 0 clonerr 0\n\tPort 1: packets 0 bytes 0 packets dropped 0 bytes dropped 0 clone 0 clonerr 0\n\tDROP: packets 0 bytes 0 packets dropped 0 bytes dropped 0 clone 0 clonerr 0\n\nTables:\n\tTable forwarding:\n\t\tHit (packets): 0\n\t\tMiss (packets): 0\n\t\tAction forward (packets): 0\n\t\tAction drop (packets): 0\n\nLearner tables:\n'"
# print(full_output)