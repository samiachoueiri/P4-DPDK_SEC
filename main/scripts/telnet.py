import telnetlib
import time

# Telnet server details
host = "0.0.0.0"
port = 8086
timeout = 1
sps = 1

# Command to send
# get_index = b"pipeline PIPELINE0 regrd reg_index_0 index 0\n"
command0 = b"pipeline PIPELINE0 regrd attack_0 index 0\n"
command1 = b"pipeline PIPELINE1 regrd attack_0 index 0\n"
command2 = b"pipeline PIPELINE2 regrd attack_0 index 0\n"
command3 = b"pipeline PIPELINE3 regrd attack_0 index 0\n"

# Function to connect to telnet server and send command
def telnet_session(host, port, timeout):
    try:
        # Connect to the telnet server
        tn = telnetlib.Telnet(host, port, timeout)
        tn.read_until(b"Escape character is", timeout)

        # tn.write(get_index)
        # output = tn.read_until(b"\n", timeout)

        tn.write(command0)
        output = tn.read_until(b"\n", timeout)
        
        while True:
            try:
                # tn.write(get_index)
                # output = tn.read_until(b"\n", timeout)
                # string_output = output.decode('utf-8')
                # index_hex = string_output.split(' ')[1].strip()
                # index_dec = int(index_hex, 16)
                # index_hex = '0x4270'

                # get_count = f"pipeline PIPELINE0 regrd ht0_0 index {index_hex}\n"
                # get_count = get_count.encode('utf-8')
                # tn.write(get_count)
                # output = tn.read_until(b"\n", timeout)
                # string_output = output.decode('utf-8')
                # count_hex = string_output.split(' ')[1]
                # count_dec = int(count_hex, 16)

                tn.write(command0)
                output = tn.read_until(b"\n", timeout)
                string_output = output.decode('utf-8')
                test0_hex = string_output.split(' ')[1].strip()

                tn.write(command1)
                output = tn.read_until(b"\n", timeout)
                string_output = output.decode('utf-8')
                test1_hex = string_output.split(' ')[1].strip()

                tn.write(command2)
                output = tn.read_until(b"\n", timeout)
                string_output = output.decode('utf-8')
                test2_hex = string_output.split(' ')[1].strip()

                tn.write(command3)
                output = tn.read_until(b"\n", timeout)
                string_output = output.decode('utf-8')
                test3_hex = string_output.split(' ')[1].strip()
                
                print("attack:","P0",test0_hex,"P1",test1_hex,"P2",test2_hex,"P3",test3_hex)
                time.sleep(1/sps)
            
            except KeyboardInterrupt:
                print("\nProcess interrupted. Closing...")
                break  # Exit the loop on interrupt

    except Exception as e:
        print(f"Error: {e}")

    finally:
        tn.close()  # Ensure tn.close() is executed

# Start the telnet session
telnet_session(host, port, timeout)
