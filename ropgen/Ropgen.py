from struct import pack

try:
    # For Python 2
    from cStringIO import StringIO
except ImportError:
    # For Python 3
    from io import StringIO


class RopGen():
    def __init__(self, endian = 'le', padding = 'A', total_length = 0):
        """
        Constructior

        :param endian: The Endianess, can be big (be) or little endian (le)
        :type endian: string

        :param padding: The filler character to be used for the exploit string
        :type padding: string

        :param total_length: The final length of the generated rop string. If this is not specified,
                            length the rop string is as big as it is necessary to encompass all values.

        :type total_length: integer
        """

        if endian != 'le' and endian != 'be':
            raise Exception('Incorrect endian specified, can be one of big (be) or little (le).')
        if len(padding) != 1:
            raise Exception('Padding byte can consist of only 1 character.')

        self.endian = endian
        self.padding = padding
        self.map = {}
        self.total_length = total_length
        self.desc_table = None


    def set_byte(self, pos, byte, desc = ''):
        """
        Sets a byte value at the specified position

        :param pos: The position where the byte will be placed
        :type pos: integer

        :param byte: The byte value
        :type byte: integer

        :param desc: Description string
        :type desc: string
        """
        
        self.map[pos] = pack('<B', byte), desc


    def set_word(self, pos, word, desc = ''):
        """
        Sets a word (2 bytes) value at the specified position

        :param pos: The position where the word will be placed
        :type pos: integer

        :param word: The word value 
        :type word: integer

        :param desc: Description string
        :type desc: string
        """

        if self.endian == 'le':
            self.map[pos] = pack('<H', word), desc
        elif self.endian == 'be':
            self.map[pos] = pack('>H', word), desc


    def set_dword(self, pos, dword, desc = ''):
        """
        Sets a dword (4 bytes) value at the specified position

        :param pos: The position where the dword will be placed
        :type pos: integer

        :param dword: The dword value 
        :type dword: integer

        :param desc: Description string
        :type desc: string
        """     

        if self.endian == 'le':
            self.map[pos] = pack('<L', dword), desc
        elif self.endian == 'be':
            self.map[pos] = pack('>L', dword), desc


    def set_qword(self, pos, qword, desc = ''):
        """
        Sets a quad word (8 bytes) value at the specified position

        :param pos: The position where the qword will be placed
        :type pos: integer

        :param qword: The dword value 
        :type qword: integer

        :param desc: Description string
        :type desc: string
        """     

        if self.endian == 'le':
            self.map[pos] = pack('<Q', qword), desc
        elif self.endian == 'be':
            self.map[pos] = pack('>Q', qword), desc


    def set_string(self, pos, sval, desc = ''):
        """
        Sets a string at the specifed position

        :param pos: The position where the string will be placed
        :type pos: integer

        :param string: The string value 
        :type sval: string

        :param desc: Description string
        :type desc: string
        """        

        self.map[pos] = sval, desc


    def build(self):
        """
        Generates and returns the rop string.

        :return: Generated rop string
        :rtype: string
        """
        curr_offs = 0
        self.desc_table = []
        buffer = StringIO()

        for pos in sorted(self.map):
            if curr_offs > pos:
                raise Exception("Parts of the rop string overlap. Please recheck")

            elif curr_offs == pos:
                val, desc = self.map[pos][0], self.map[pos][1]
                self.desc_table.append((curr_offs, desc, len(val)))
                buffer.write(str(val))
                curr_offs += len(val)

            elif curr_offs < pos:
                num_padding_bytes = pos - curr_offs
                buffer.write(self.padding * num_padding_bytes)
                self.desc_table.append((curr_offs, 'Padding Bytes', num_padding_bytes))
                curr_offs = pos

                val, desc = self.map[pos][0], self.map[pos][1]
                self.desc_table.append((curr_offs, desc, len(val)))
                buffer.write(str(val))
                curr_offs += len(val)

        # Pad with filler bytes
        if curr_offs < self.total_length:
            num_padding_bytes = self.total_length - curr_offs
            buffer.write(self.padding * num_padding_bytes)
            self.desc_table.append((curr_offs, 'Padding Bytes', num_padding_bytes))

        return buffer.getvalue()        


    def summarize(self):
        """
        Summarizes the rop string in the form of a nice table.

        :return: Generated table
        :rtype: string
        """

        from texttable import Texttable

        if self.desc_table:
            table = Texttable()

            table.set_cols_align(["l", "l", "c"])
            table.header(["Offset", "Content description", "Length in bytes"])
            for e in self.desc_table:
                table.add_row([e[0], e[1], e[2]])

            return table.draw()
