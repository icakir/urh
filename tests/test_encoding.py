import unittest

from urh.signalprocessing.encoding import encoding

class TestDecoding(unittest.TestCase):
    # Testmethode muss immer mit Präfix test_* starten
    def test_carrier(self):
        e = encoding()

        # Test 1
        e.carrier = "----1....1**"  # or "....1....101", ...
        original_inpt = e.str2bit("000010000100111111111100")
        inpt = original_inpt.copy()
        #print("\nOriginal:", inpt)
        output, err = e.code_carrier(True, inpt)
        #print("Decoded: ", output, err)
        newinpt, err = e.code_carrier(False, output)
        #print("Encoded: ", newinpt, err)
        self.assertEqual(original_inpt, newinpt)

    def test_enocean(self):
        e = encoding()


        received = "01010101011010011110101011101110111011101110011000101110101000101110111011011101110100"
        received = "00010101010110100111101010111011101110111011100110001011101010001011101110110111011101000"
        received2 = "000010101010110101001101110111011101110111011100110001011101010001011101110110111100101000"
        # First step is invert the received bits!!!
        #received = "10101010 1001 011000010101 000100010001 000100011001 110100010101 110100010001 0010001000 1011"
        preamble = "10101010"
        sof = "1001"
        eof = "1011"

        self.assertIn(preamble, received)
        self.assertIn(sof, received)
        self.assertIn(eof, received)

        # Preamble/SOF/EOF remain unchanged
        expected_result = "11" + preamble + sof + "01100001 00000000 00000010 11000001 11000000 00100100" + eof + "1"
        expected_result2 = "111" + preamble + sof + "01010000 00000000 00000010 11000001 11000000 00100010" + eof + "1"

        decoded, err = e.code_enocean(True, e.str2bit(received.replace(" ","")))
        decoded2, err2 = e.code_enocean(True, e.str2bit(received2.replace(" ", "")))
        self.assertEqual(err, 0)
        self.assertEqual(err2, 0)
        reencoded, err = e.code_enocean(False, decoded)
        reencoded2, err2 = e.code_enocean(False, decoded2)
        self.assertEqual(err, 0)
        self.assertEqual(err2, 0)

        self.assertEqual(decoded, e.str2bit(expected_result.replace(" ", "")))
        self.assertEqual(reencoded, e.str2bit(received))
        self.assertEqual(decoded2, e.str2bit(expected_result2.replace(" ", "")))
        self.assertEqual(reencoded2, e.str2bit(received2))

        received = e.str2bit("00001010010101111111000")
        expected_result = e.str2bit("1010010101111111000")
        e.cutmode = 0
        e.cutmark = [True, False, True, False]
        decoded, err = e.code_cut(True, received)
        self.assertEqual(decoded, expected_result)

        received = e.str2bit("00001010010101111111000")
        expected_result = e.str2bit("00001010")
        e.cutmode = 1
        e.cutmark = [True, False, True, False]
        decoded, err = e.code_cut(True, received)
        self.assertEqual(decoded, expected_result)

        received = e.str2bit("00001010010101111111000")
        expected_result = e.str2bit("001010010101111111000")
        e.cutmode = 2
        e.cutmark = 2
        decoded, err = e.code_cut(True, received)
        self.assertEqual(decoded, expected_result)

        received = e.str2bit("00001010010101111111000")
        expected_result = e.str2bit("000")
        e.cutmode = 3
        e.cutmark = 2
        decoded, err = e.code_cut(True, received)
        self.assertEqual(decoded, expected_result)

        received = e.str2bit("00001010010101111111000")
        expected_result = e.str2bit("00001010010101111111000")
        e.cutmode = 0
        e.cutmark = [True, False, True, False, True, False]
        decoded, err = e.code_cut(True, received)
        self.assertEqual(decoded, expected_result)