import unittest

from aioice import Candidate


class CandidateTest(unittest.TestCase):
    def test_can_pair_ipv4(self):
        candidate_a = Candidate.from_sdp(
            '6815297761 1 udp 659136 1.2.3.4 31102 typ host generation 0')
        candidate_b = Candidate.from_sdp(
            '6815297761 1 udp 659136 1.2.3.4 12345 typ host generation 0')
        self.assertTrue(candidate_a.can_pair_with(candidate_b))

    def test_can_pair_ipv6(self):
        candidate_a = Candidate.from_sdp(
            '6815297761 1 udp 659136 2a02:0db8:85a3:0000:0000:8a2e:0370:7334 31102'
            ' typ host generation 0')
        candidate_b = Candidate.from_sdp(
            '6815297761 1 udp 659136 2a02:0db8:85a3:0000:0000:8a2e:0370:7334 12345'
            ' typ host generation 0')
        self.assertTrue(candidate_a.can_pair_with(candidate_b))

    def test_cannot_pair_ipv4_ipv6(self):
        candidate_a = Candidate.from_sdp(
            '6815297761 1 udp 659136 1.2.3.4 31102 typ host generation 0')
        candidate_b = Candidate.from_sdp(
            '6815297761 1 udp 659136 2a02:0db8:85a3:0000:0000:8a2e:0370:7334 12345'
            ' typ host generation 0')
        self.assertFalse(candidate_a.can_pair_with(candidate_b))

    def test_cannot_pair_different_components(self):
        candidate_a = Candidate.from_sdp(
            '6815297761 1 udp 659136 1.2.3.4 31102 typ host generation 0')
        candidate_b = Candidate.from_sdp(
            '6815297761 2 udp 659136 1.2.3.4 12345 typ host generation 0')
        self.assertFalse(candidate_a.can_pair_with(candidate_b))

    def test_from_to_sdp(self):
        candidate = Candidate.from_sdp(
            '6815297761 1 udp 659136 1.2.3.4 31102 typ host generation 0')
        self.assertEqual(candidate.foundation, '6815297761')
        self.assertEqual(candidate.component, 1)
        self.assertEqual(candidate.transport, 'udp')
        self.assertEqual(candidate.priority, 659136)
        self.assertEqual(candidate.host, '1.2.3.4')
        self.assertEqual(candidate.port, 31102)
        self.assertEqual(candidate.type, 'host')
        self.assertEqual(candidate.generation, 0)

        self.assertEqual(
            candidate.to_sdp(),
            '6815297761 1 udp 659136 1.2.3.4 31102 typ host generation 0')

    def test_from_sdp_no_generation(self):
        with self.assertRaises(ValueError):
            Candidate.from_sdp('6815297761 1 udp 659136 1.2.3.4 31102 typ host')

    def test_from_sdp_truncated(self):
        with self.assertRaises(ValueError):
            Candidate.from_sdp('6815297761 1 udp 659136 1.2.3.4 31102 typ')
