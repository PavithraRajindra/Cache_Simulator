import tkinter as tk
import random

# Constants
CPU_ADDRESS_BITS = 16
MAIN_MEMORY_SIZE = 64 * 1024  # 64 kB
L1_CACHE_SIZE = 8 * 1024  # 8 kB
L1_LINE_SIZE = 64  # bytes
L1_CACHE_LINES = 128
L1_VICTIM_CACHE_LINES = 4
L2_CACHE_SIZE = 16 * 1024  # 16 kB
L2_CACHE_LINES = 256
WORD_SIZE = 4  # bytes

# Initialize cache data structures with None to represent empty cache lines
l1_cache = [None for _ in range(L1_CACHE_LINES)]
l1_victim_cache = [None for _ in range(L1_VICTIM_CACHE_LINES)]
l2_cache = [None for _ in range(L2_CACHE_LINES)]
main_memory = [i for i in range(MAIN_MEMORY_SIZE // WORD_SIZE)]

# Initialize tkinter window
window = tk.Tk()
window.title("Cache Mapping Simulator")
window.configure(bg="#333333")


#____________________________CPU_GUI______________________________________________
# Create CPU cpu_frame with canvas
cpu_frame = tk.Frame(window, bg="pink", bd=0, relief="flat")
cpu_frame.grid(row=1, column=0, padx=10, pady=10)
label = tk.Label(cpu_frame, text="CPU", font=("Helvetica", 10, "bold"), bg="#333333", fg="pink")
label.grid(row=0, column=0, padx=10, pady=5)
canvas = tk.Canvas(cpu_frame, width=200, height=100, bg="pink", bd=0, highlightthickness=0)
canvas.grid(row=1, column=0, padx=5, pady=5)

#____________________________L1_CACHE_GUI________________________________________
# Create L1 cache text box
l1_cache_label = tk.Label(window, text="L1 Cache", font=("Helvetica", 10, "bold"), bg="#333333", fg="white")
l1_cache_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
l1_cache_text = tk.Text(window, height=20, width=20, bg="light blue")
l1_cache_text.grid(row=1, column=1, padx=10, pady=10)
for i in range(L1_CACHE_SIZE // L1_LINE_SIZE):
    line_data = l1_cache[i] if l1_cache[i] else "Empty"
    l1_cache_text.insert(tk.END, f'Line {i}: {line_data}\n')

# Function to update the L1 cache display in the GUI
def update_l1_cache_display(line_bits, data):
    line_no = line_bits
    l1_cache[line_no]=data
    l1_cache_text.delete('1.0', tk.END)
    
    # Re-populate the text widget with the updated cache data
    for index, line_data in enumerate(l1_cache):
        if line_data is None:
            line_data = "Empty"
        l1_cache_text.insert(tk.END, f'Line {index}: {line_data}\n')

#_____________________________VICTIM_CACHE_GUI___________________________________
# Create Victim cache text box
victim_cache_label = tk.Label(window, text="Victim Cache", font=("Helvetica", 10, "bold"), bg="#333333", fg="white")
victim_cache_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
victim_cache_text = tk.Text(window, height=7, width=20, bg="light blue")
victim_cache_text.grid(row=1, column=2, padx=10, pady=10)
for i in range(L1_VICTIM_CACHE_LINES):
    line_data = l1_victim_cache[i] if l1_victim_cache[i] else "Empty"
    victim_cache_text.insert(tk.END, f'Line {i}: {line_data}\n')

# Function to update the Victim cache display in the GUI
def update_victim_cache_display(line_index, data):
    l1_victim_cache[line_index] = data
    # Clear existing cache content
    victim_cache_text.delete('1.0', tk.END)
    
    # Re-populate the text widget with the updated cache data
    for i in range(L1_VICTIM_CACHE_LINES):
        line_data = l1_victim_cache[i] if l1_victim_cache[i] else "Empty"
        victim_cache_text.insert(tk.END, f'Line {i}: {line_data}\n')

#_____________________________L2_CACHE_GUI___________________________________
# Create L2 cache text box
l2_cache_label = tk.Label(window, text="L2 Cache", font=("Helvetica", 10, "bold"), bg="#333333", fg="white")
l2_cache_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
l2_cache_text = tk.Text(window, height=20, width=20, bg="light blue")
l2_cache_text.grid(row=1, column=3, padx=10, pady=10)
for i in range(L2_CACHE_LINES):
    line_data = l2_cache[i] if l2_cache[i] else "Empty"
    l2_cache_text.insert(tk.END, f'Line {i}: {line_data}\n')

# Function to update the L2 cache display in the GUI
def update_l2_cache_display():
    # Clear existing L2 cache content
    l2_cache_text.delete('1.0', tk.END)

    # Re-populate the text widget with the updated cache data
    for index, line_data in enumerate(l2_cache):
        if line_data is None:
            line_data = "Empty"
        l2_cache_text.insert(tk.END, f'Line {index}: {line_data}\n')

#_____________________________MAIN_MEMORY_GUI___________________________________
# Create text box to display main memory contents
main_memory_label = tk.Label(window, text="Main Memory", font=("Helvetica", 10, "bold"), bg="#333333", fg="white")
main_memory_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")
main_memory_text = tk.Text(window, height=20, width=30, bg="light blue")
main_memory_text.grid(row=1, column=4, padx=10, pady=10)
# Display binary addresses in the main memory box
for i in range(MAIN_MEMORY_SIZE // WORD_SIZE):
    address_binary = f"{i:016b}"
    main_memory_text.insert(tk.END, address_binary+'\n')

#_____________________________BITS_GUI__________________________________________
# Create text box to display the physical address, tag bits, line bits, and byte offset
address_label = tk.Label(window, text="Physical Address: ", fg="#FFFFFF", bg="#333333")
address_label.grid(row=1, column=0, padx=55, pady=3, sticky="w")

physical_address_var = tk.StringVar()
physical_address_var.set("")
address_display_label = tk.Label(cpu_frame, textvariable=physical_address_var, fg="#FFFFFF", bg="#333333")
address_display_label.grid(row=1, column=0, padx=45, pady=10, sticky="w")

tag_bits_label = tk.Label(window, text="Tag Bits: ", fg="#FFFFFF", bg="#333333")
tag_bits_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

tag_bits_var = tk.StringVar()
tag_bits_var.set("")
tag_bits_display_label = tk.Label(window, textvariable=tag_bits_var, fg="#FFFFFF", bg="#333333")
tag_bits_display_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

line_number_label = tk.Label(window, text="Line Bits: ", fg="#FFFFFF", bg="#333333")
line_number_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

line_number_var = tk.StringVar()
line_number_var.set("")
line_number_display_label = tk.Label(window, textvariable=line_number_var, fg="#FFFFFF", bg="#333333")
line_number_display_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

bit_offset_label = tk.Label(window, text="Byte Offest: ", fg="#FFFFFF", bg="#333333")
bit_offset_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

bit_offset_var = tk.StringVar()
bit_offset_var.set("")
bit_offset_display_label = tk.Label(window, textvariable=bit_offset_var, fg="#FFFFFF", bg="#333333")
bit_offset_display_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Create cache result text box
cache_result_text = tk.Text(window, height=6, width=50)
cache_result_text.grid(row=6, column=0, columnspan=5, padx=10, pady=(0, 10))

# Function to fetch a random integer between min and max (inclusive)
def get_random_int(min_value, max_value):
    return random.randint(min_value, max_value)


def fetch_from_L1_cache(address):
    # Calculate cache index, tag bits, and byte offset for L1 cache
    line_bits = (address % (L1_CACHE_LINES * L1_LINE_SIZE)) // L1_LINE_SIZE
    tag = address // (L1_CACHE_LINES * L1_LINE_SIZE)
    byte_offset = address % L1_LINE_SIZE

    # Update labels with address details
    physical_address_var.set(f"{address:016b}")
    tag_bits_var.set(f"{tag:03b}")
    line_number_var.set(f"{line_bits:07b}")
    bit_offset_var.set(f"{byte_offset:06b}")

    # Check if cache index is within the valid range
    if 0 <= line_bits < L1_CACHE_LINES:
        # Check L1 cache
        if l1_cache[line_bits] is not None and l1_cache[line_bits] == tag:
            # Cache hit in L1
            cache_result_text.insert(tk.END, "L1 Cache Hit!\n", "hit")
            # Update LRU access time for the line (move to the head of the linked list)
            update_lru_in_l1_cache(line_bits)
            return l1_cache[line_bits]
        else:
            # L1 cache miss
            cache_result_text.insert(tk.END, "L1 Cache Miss!\n", "miss")
            return fetch_from_victim_cache(address)
    else:
        # Invalid cache index
        cache_result_text.insert(tk.END, "Invalid L1 Cache Index!\n", "miss")
        return None



def update_lru_in_l1_cache(cache_line_index):
    # If there's no LRU linked list implemented, create one here
    # This example uses a simple Python list to represent the LRU order
    if not l1_victim_cache:
        l1_victim_cache.append(cache_line_index)
    else:
        # Move the accessed line to the head (most recently used)
        if cache_line_index in l1_victim_cache:
            l1_victim_cache.remove(cache_line_index)
        l1_victim_cache.insert(0, cache_line_index)

def fetch_from_victim_cache(address):
    victim_tag_bits = address % L1_VICTIM_CACHE_LINES

    if l1_victim_cache:
        for i in range(len(l1_victim_cache)):
            if l1_victim_cache[i] == victim_tag_bits:
                # Victim cache hit
                cache_result_text.insert(tk.END, "Victim Cache Hit!\n", "hit")
                data = l1_victim_cache[i]
                update_victim_cache_display(i, data)
                return data

        cache_result_text.insert(tk.END, "Victim Cache Miss!\n", "miss")
        victim_line_to_evict = replace_line_in_victim_cache(address)
        if victim_line_to_evict is not None:
            # Remove the evicted line from the victim cache
            evicted_data = l1_victim_cache.pop(victim_line_to_evict)
            # Add the new line to the victim cache
            l1_victim_cache.insert(victim_line_to_evict, fetch_from_L2_cache(address))
            update_victim_cache_display(victim_line_to_evict, l1_victim_cache[victim_line_to_evict])
            return l1_victim_cache[victim_line_to_evict]
        else:
            cache_result_text.insert(tk.END, "No eviction needed in Victim Cache!\n", "miss")
            return fetch_from_L2_cache(address)
    else:
        cache_result_text.insert(tk.END, "Victim Cache Empty!\n", "miss")
        return fetch_from_L2_cache(address)

def fetch_from_L2_cache(address):
    # Calculate set index, tag, and offset
    set_index = (address // WORD_SIZE) % (L2_CACHE_LINES // 4)
    tag = address // ((L2_CACHE_LINES // 4) * WORD_SIZE)
    
    if l2_cache:
        l2_hit = False
        for i in range(4):
            cache_line_index = set_index * 4 + i
            if l2_cache[cache_line_index] == tag:
                # L2 cache hit
                l2_hit = True
                data = l2_cache[cache_line_index]
                fetch_from_L1_cache(address)  # Update L1 cache on L2 hit (optional)
                return data
        if not l2_hit:
            # L2 cache miss
            cache_result_text.insert(tk.END, "L2 Cache Miss!\n", "miss")
            data = fetch_from_main_memory(address)  # Fetch from main memory
            victim_line_to_evict = replace_line_in_L2_cache(set_index)
            l2_cache[victim_line_to_evict] = data
            update_l2_cache_display()
            update_l1_cache_display((address % (L1_CACHE_LINES * L1_LINE_SIZE)) // L1_LINE_SIZE, data)  # Update L1 cache display
            # Ensure we don't enter an infinite loop
            return data


def replace_line_in_victim_cache(address):
    # Implement LRU eviction policy for the victim cache
    if not l1_victim_cache:
        return None  # No eviction needed if victim cache is empty

    # Least Recently Used line is at the end of the LRU list
    return len(l1_victim_cache) - 1

def replace_line_in_L2_cache(set_index):
    # Implement eviction policy for L2 cache (e.g., LRU, FIFO)
    # Here, we use LRU

    # Identify the starting and ending line indices within the set
    start_line_index = set_index * 4
    end_line_index = start_line_index + 3

    # Maintain a separate LRU list for each set in L2
    # (This can be optimized using a single LRU list with additional logic)
    lru_list = [i for i in range(start_line_index, end_line_index + 1)]

    # Least Recently Used line is at the end of the LRU list for the set
    victim_line_to_evict = lru_list[-1]
    lru_list.remove(victim_line_to_evict)
    return victim_line_to_evict  # Return the line index to be evicted

def fetch_from_main_memory(address):
    word_index = address // WORD_SIZE
    cache_result_text.insert(tk.END, "Found in Main Memory! Moving to Cache\n", "hit")
    data = random.randint(0, 9)
    return data

def access_memory():
    cache_result_text.delete(1.0, tk.END)
    address = get_random_int(0, MAIN_MEMORY_SIZE - 1)
    data = fetch_from_L1_cache(address)

# Create Access Memory button
access_memory_button = tk.Button(window, text="Access Memory", command=access_memory, bg="light green", fg="#333333",
                                  bd=0, padx=10, pady=5)
access_memory_button.grid(row=7, column=0, columnspan=5, padx=10, pady=(0, 10))

# Configure text box styles
cache_result_text.tag_config("hit", background="green", foreground="white")
cache_result_text.tag_config("miss", background="red", foreground="white")


# Start the tkinter event loop
window.mainloop()
