import time
import socket
import json
from datasketch import HyperLogLog

def is_valid_ip(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False

def load_ips(filename):
    ips = []
    try:
        with open(filename, 'r') as f:
            print(f"Successfully opened {filename}")
            line_count = 0
            valid_ip_count = 0
            
            for line in f:
                line_count += 1
                try:
                    # Parse the JSON content of each line
                    log_entry = json.loads(line)
                    
                    # Extract the remote_addr field which contains the IP
                    ip_candidate = log_entry.get('remote_addr', '')
                    
                    if ip_candidate and is_valid_ip(ip_candidate):
                        valid_ip_count += 1
                        ips.append(ip_candidate)
                    
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON on line {line_count}")
                    continue
        print(f"Finished processing {line_count} lines, found {valid_ip_count} valid IPs")

        return ips
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        return []
    except Exception as e:
        print(f"Error while reading file: {str(e)}")
        return []

def exact_count(ips):
    count = len(set(ips))
    print(f"Exact count found {count} unique IPs")
    return count

def hyperloglog_count(ips, p=14):
    hll = HyperLogLog(p=p)
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    count = hll.count()
    print(f"HyperLogLog estimated {count} unique IPs")
    return count

def main():
    print("Processing log file...")
    ips = load_ips('lms-stage-access.log')
    
    if not ips:
        print("Error: No valid IPs were loaded from the log file")
        return
    
    # Exact count with timing
    start_time = time.time()
    exact = exact_count(ips)
    exact_time = time.time() - start_time
    
    # HyperLogLog estimation with timing
    start_time = time.time()
    hll = hyperloglog_count(ips)
    hll_time = time.time() - start_time
    
    # Results presentation
    print("\nРезультати порівняння:")
    print("                       Точний підрахунок   HyperLogLog")
    print(f"Унікальні елементи           {exact:8.1f}    {hll:8.1f}")
    print(f"Час виконання (сек.)         {exact_time:8.2f}    {hll_time:8.2f}")

if __name__ == "__main__":
    main()