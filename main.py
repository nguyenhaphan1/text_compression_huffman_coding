from collections import Counter
import os

class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right


def huffman_code_tree(node, binString=''):
    '''
    Function to find Huffman Code
    '''
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d


def make_tree(nodes):
    '''
    Function to make tree
    :param nodes: Nodes
    :return: Root of the tree
    '''
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


def encode(string, encoding):
    if not string:
        return
    new_string = ''
    for c in string:
        new_string += encoding[c]
    return new_string


def decode(encoded_string, root):
    decoded_string = ''
    node = root
    for c in encoded_string:
        if c == '0':
            node = node.left
        else:
            node = node.right
        if type(node) is str:
            decoded_string += node
            node = root

    return decoded_string


def decompression(input_path):
    # Đọc file key để lấy dữ liệu decode
    decompression_file_key = open(input_path + '_key.txt', 'r')
    lines = decompression_file_key.readlines()
    decompression_file_key.close()
    encode_list = []
    for line in lines:
        line = line.split()
        k, v = line[0], line[1]
        encode_list.append((k, int(v)))
    new_freq = format_file_to_encode_list(encode_list)
    new_root = make_tree(new_freq)
    #     for i in new_freq:
    #         print(i)
    # Đọc file nén
    decompression_file = open(input_path + ".bin", 'rb')
    bit_string = ''
    byte = decompression_file.read(1)
    while byte:
        byte = ord(byte)
        bits = bin(byte)[2:]
        if len(bits) < 8:
            numb_of_zero = 8 - len(bits)
        bits = bits.rjust(8, '0')
        print(bits)
        bit_string += bits
        byte = decompression_file.read(1)
    if int(bits, 2) == 0:
        bit_string = bit_string[:-8]
    else:
        bit_string = bit_string[:-8]
        #     print(len(bit_string))
        addition_zero = int(bits, 2)
        string = bit_string[-8:]
        string = list(string)
        string = "".join(string[addition_zero:])
        print(string)
        bit_string = bit_string[:-8] + string
    #     print(bit_string)
    decompression_file.close()
    file_giai_nen = input('Enter file name:')
    new_file = open(file_giai_nen, 'w')
    new_file.write(decode(bit_string, new_root))
    return decode(bit_string, new_root)


def build_byte_array(encoded_text):
    array = []
    for i in range(0,len(encoded_text) , 8):
        byte = encoded_text[i:i+8]
        array.append(int(byte,2))
    array.append((8 - len(byte)))
    return array


def compression(string):
    freq = dict(Counter(string))
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    encoded = encode(string, encoding)
    final_bytes = bytes(build_byte_array(encoded))
    compress_file = input('Enter file name to save:')
    output = open(compress_file + ".bin", 'w+b')
    output.write(final_bytes)
    output.close()
    # Tạo file chứ key để sau này decode
    key_freq = format_key_to_file(freq.copy())
    key_folder = open(compress_file + '_key.txt', 'w')
    for i in key_freq:
        a = i[0] + ' ' + str(i[1])
        key_folder.write(a + '\n')
    key_folder.close()
    print("Successfully compress file!")
    return encoded

def format_key_to_file(key_freq):
    for i in key_freq:
        t = list(i)
        if t[0] == ' ':
            t[0] = '\\t'
            key_freq[key_freq.index(i)] = tuple(t)
            continue
        if t[0] == '\n':
            t[0] = '\\n'
            key_freq[key_freq.index(i)] = tuple(t)
            continue
        i = tuple(t)
    return key_freq


def format_file_to_encode_list(encode_list):
    for i in encode_list:
        t = list(i)
        if t[0] == '\\t':
            t[0] = ' '
            encode_list[encode_list.index(i)] = tuple(t)
            continue
        if t[0] == '\\n':
            t[0] = '\n'
            encode_list[encode_list.index(i)] = tuple(t)
            continue
        i = tuple(t)
    return encode_list


if __name__ == '__main__':
    fileName = ''
    choice = None
    f = None
    fileName = None
    string = None
    encoded = None
    decoded = None
    node = None
    compress_file = None
    while (True):
        print("\n------------ Text file compression and decompression with Huffman algorithm ------------\n")
        print("1. Read .txt File")
        print("2. Show File")
        print("3. Show compress form")
        print("4. Compress File")
        print("5. Decompress File")
        print("6. Exit")
        while (True):
            try:
                choice = int(input("Enter your choice(1-6):"))
                if choice < 1 or choice > 6:
                    raise Exception
                break
            except Exception as e:
                print('Wrong input number, number must be an integer in range 1-4!')
        if choice == 1:
            while (True):
                fileName = input('Enter .txt file name:')
                if fileName.endswith('.txt'):
                    break
                print("Wrong file name!. File name must format 'file_name.txt' (i.e: file1.txt)")
            try:
                f = open(fileName)
                string = f.read()
                f.close()
                print("File is exist, successfully open file!")
            except Exception as e:
                print(e)
        elif choice == 2:
            if string is None:
                print('No such file found!')
                continue
            print(string)
        elif choice == 3:
            if encoded:
                print(encoded)
            else:
                print("You haven't compress any file, please compress a file to use this feature!")
        elif choice == 4:
            if fileName == None:
                print("No file was choosen, please choose a file to use this feature")
                continue
            encoded = compression(string)
        elif choice == 5:
            decompress_file_name = input('Enter file name to decompress:')

            if not os.path.isfile(decompress_file_name + '.bin') :
                print('No such compression file name ' + decompress_file_name + '.bin to decompress')
                continue
            if not os.path.isfile(decompress_file_name + '_key'+'.txt') :
                print("This compression file doesn't have key to decompress!")
                continue
            decoded = decompression(decompress_file_name)
            print('Successfully decode file, file after decoded:')
            print(decoded)
        elif choice == 6:
            print("Have a nice day!")
            break