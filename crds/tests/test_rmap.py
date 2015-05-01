"""This module contains doctests and unit tests which exercise some of the more
complex features of the basic rmap infrastructure.

"""

from __future__ import division # confidence high
from __future__ import with_statement
from __future__ import print_function

import os
from pprint import pprint as pp

from crds import rmap, log, exceptions
from crds.tests import CRDSTestCase

from nose.tools import assert_raises, assert_true

# ==================================================================================

def test_get_derived_from():
    """
    >>> r = rmap.get_cached_mapping("hst_acs_flshfile_0252.rmap")
    >>> r.get_derived_from().name
    'hst_acs_flshfile_0251.rmap'
    """

def test_get_derived_from_created():
    """
    >>> log.set_test_mode()
    >>> p = rmap.get_cached_mapping("hst.pmap")
    >>> p.get_derived_from()
    CRDS  : INFO     Skipping derivation checks for root mapping 'hst.pmap' derived_from = 'created by hand 12-23-2011'
    """
def test_get_derived_from_phony():
    """
    >>> log.set_test_mode()
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_phony_derive.rmap")
    >>> r.get_derived_from()
    CRDS  : WARNING  Parent mapping for 'hst_acs_darkfile_phony_derive.rmap' = 'phony.rmap' does not exist.
    """

def test_missing_required_header_key():
    """
    >>> r = rmap.load_mapping("data/hst_acs_darkfile_missing_key.rmap")
    Traceback (most recent call last):
    ...
    MissingHeaderKeyError: Required header key 'mapping' is missing.
    """

def test_rmap_missing_references():
    """
    These are all missing because there is no reference file cache in this mode.

    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_comment.rmap")
    >>> pp(r.missing_references())
    ['lcb12060j_drk.fits',
     'n3o1022cj_drk.fits',
     'n3o1022ej_drk.fits',
     'n3o1022fj_drk.fits',
     'n3o1022hj_drk.fits',
     'n3o1022ij_drk.fits',
     'n3o1022kj_drk.fits',
     'n3o1022lj_drk.fits',
     'r1u1415ij_drk.fits',
     'r1u1415kj_drk.fits',
     'r1u1415mj_drk.fits']
    """

def test_rmap_minimum_header():
    """
    >>> p = rmap.get_cached_mapping("hst.pmap")
    >>> pp(p.get_minimum_header("data/j8bt05njq_raw.fits"))
    {'APERTURE': 'HRC',
     'ATODCORR': 'OMIT',
     'BIASCORR': 'PERFORM',
     'CCDAMP': 'C',
     'CCDCHIP': 'UNDEFINED',
     'CCDGAIN': '2.0',
     'CRCORR': 'OMIT',
     'DARKCORR': 'PERFORM',
     'DATE-OBS': '2002-04-13',
     'DETECTOR': 'HRC',
     'DQICORR': 'PERFORM',
     'DRIZCORR': 'PERFORM',
     'FILTER1': 'F555W',
     'FILTER2': 'CLEAR2S',
     'FLASHCUR': 'OFF',
     'FLATCORR': 'PERFORM',
     'FLSHCORR': 'OMIT',
     'FW1OFFST': '0.0',
     'FW2OFFST': '0.0',
     'FWSOFFST': '0.0',
     'GLINCORR': 'UNDEFINED',
     'INSTRUME': 'ACS',
     'LTV1': '19.0',
     'LTV2': '0.0',
     'NUMCOLS': 'UNDEFINED',
     'NUMROWS': 'UNDEFINED',
     'OBSTYPE': 'IMAGING',
     'PCTECORR': 'UNDEFINED',
     'PHOTCORR': 'PERFORM',
     'REFTYPE': 'UNDEFINED',
     'SHADCORR': 'OMIT',
     'SHUTRPOS': 'B',
     'TIME-OBS': '18:16:35',
     'XCORNER': 'UNDEFINED',
     'YCORNER': 'UNDEFINED'}
    """
    


def test_rmap_str():
    """
    >>> r = rmap.get_cached_mapping("data/hst_cos_bpixtab_0252.rmap")
    >>> print(str(r), end="")
    header = {
        'derived_from' : 'hst_cos_bpixtab_0251.rmap',
        'filekind' : 'BPIXTAB',
        'instrument' : 'COS',
        'mapping' : 'REFERENCE',
        'name' : 'hst_cos_bpixtab_0252.rmap',
        'observatory' : 'HST',
        'parkey' : (('DETECTOR',), ('DATE-OBS', 'TIME-OBS')),
        'reffile_format' : 'TABLE',
        'reffile_required' : 'NONE',
        'reffile_switch' : 'NONE',
        'rmap_relevance' : 'ALWAYS',
        'sha1sum' : 'd2024dade52a406af70fcdf27a81088004d67cae',
    }
    <BLANKLINE>
    selector = Match({
        ('FUV',) : UseAfter({
            '1996-10-01 00:00:00' : 's7g1700dl_bpix.fits',
            '2009-05-11 00:00:00' : 'z1r1943fl_bpix.fits',
        }),
        ('NUV',) : UseAfter({
            '1996-10-01 00:00:00' : 's7g1700pl_bpix.fits',
            '2009-05-11 00:00:00' : 'uas19356l_bpix.fits',
        }),
    })
    """

def test_rmap_obs_package():
    """
    >>> p = rmap.get_cached_mapping("data/hst_acs_darkfile.rmap")
    >>> p.obs_package.__name__
    'crds.hst'
    """
    
def test_rmap_format_with_comment():
    '''
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_comment.rmap")
    >>> print(r.comment, end="")
    <BLANKLINE>
    This is a block comment which can be used to store additional metadata
    about the state and evolution of this type and files.

    >>> print(r, end="")
    header = {
        'derived_from' : 'generated from CDBS database 2013-01-11 13:58:14.664182',
        'filekind' : 'DARKFILE',
        'instrument' : 'ACS',
        'mapping' : 'REFERENCE',
        'name' : 'hst_acs_darkfile_comment.rmap',
        'observatory' : 'HST',
        'parkey' : (('DETECTOR', 'CCDAMP', 'CCDGAIN'), ('DATE-OBS', 'TIME-OBS')),
        'parkey_relevance' : {
            'ccdamp' : '(DETECTOR != "SBC")',
            'ccdgain' : '(DETECTOR != "SBC")',
        },
        'rmap_relevance' : 'ALWAYS',
        'sha1sum' : '0b3af86642812a1af65b77d429886e186acef915',
    }
    <BLANKLINE>
    comment = """
    This is a block comment which can be used to store additional metadata
    about the state and evolution of this type and files.
    """
    <BLANKLINE>
    selector = Match({
        ('HRC', 'A|ABCD|AD|B|BC|C|D', '1.0|2.0|4.0|8.0') : UseAfter({
            '1992-01-01 00:00:00' : 'lcb12060j_drk.fits',
            '2002-03-01 00:00:00' : 'n3o1022cj_drk.fits',
            '2002-03-18 00:00:00' : 'n3o1022ej_drk.fits',
            '2002-03-19 00:34:31' : 'n3o1022fj_drk.fits',
            '2002-03-20 00:34:32' : 'n3o1022hj_drk.fits',
            '2002-03-21 00:34:31' : 'n3o1022ij_drk.fits',
            '2002-03-22 00:34:30' : 'n3o1022kj_drk.fits',
            '2002-03-23 00:34:28' : 'n3o1022lj_drk.fits',
            '2007-01-21 02:09:05' : 'r1u1415ij_drk.fits',
            '2007-01-22 00:40:13' : 'r1u1415kj_drk.fits',
            '2007-01-26 00:07:33' : 'r1u1415mj_drk.fits',
        }),
    })
    '''

def test_rmap_missing_checksum():
    """
    >>> r = rmap.ReferenceMapping.from_string('''
    ... header = {
    ...    'derived_from' : 'generated from CDBS database 2013-01-11 13:58:14.664182',
    ...    'filekind' : 'DARKFILE',
    ...    'instrument' : 'ACS',
    ...    'mapping' : 'REFERENCE',
    ...    'name' : 'hst_acs_darkfile_comment.rmap',
    ...    'observatory' : 'HST',
    ...    'parkey' : (('DETECTOR', 'CCDAMP', 'CCDGAIN'), ('DATE-OBS', 'TIME-OBS')),
    ... }
    ...
    ... selector = Match({
    ...    ('HRC', 'A|ABCD|AD|B|BC|C|D', '1.0|2.0|4.0|8.0') : UseAfter({
    ...        '1992-01-01 00:00:00' : 'lcb12060j_drk.fits',
    ...        '2002-03-01 00:00:00' : 'n3o1022cj_drk.fits',
    ...     }),
    ... })
    ... ''')
    Traceback (most recent call last):
    ...
    ChecksumError: sha1sum is missing in '(noname)'
    """

def test_rmap_warn_checksum():
    """
    >>> r = rmap.ReferenceMapping.from_string('''
    ... header = {
    ...    'derived_from' : 'generated from CDBS database 2013-01-11 13:58:14.664182',
    ...    'filekind' : 'DARKFILE',
    ...    'instrument' : 'ACS',
    ...    'mapping' : 'REFERENCE',
    ...    'name' : 'hst_acs_darkfile_comment.rmap',
    ...    'observatory' : 'HST',
    ...    'parkey' : (('DETECTOR', 'CCDAMP', 'CCDGAIN'), ('DATE-OBS', 'TIME-OBS')),
    ...    'sha1sum' : "something bad",
    ... }
    ...
    ... selector = Match({
    ...    ('HRC', 'A|ABCD|AD|B|BC|C|D', '1.0|2.0|4.0|8.0') : UseAfter({
    ...        '1992-01-01 00:00:00' : 'lcb12060j_drk.fits',
    ...        '2002-03-01 00:00:00' : 'n3o1022cj_drk.fits',
    ...     }),
    ... })
    ... ''', ignore_checksum='warn')
    CRDS  : WARNING  Checksum error : sha1sum mismatch in '(noname)'
    """

def test_rmap_todict():
    """
    >>> r = rmap.get_cached_mapping("data/hst_cos_bpixtab_0252.rmap")
    >>> pp(r.todict())
    {'header': LowerCaseDict({'observatory': 'HST', 'name': 'hst_cos_bpixtab_0252.rmap', 'reffile_required': 'NONE', 'parkey': (('DETECTOR',), ('DATE-OBS', 'TIME-OBS')), 'mapping': 'REFERENCE', 'filekind': 'BPIXTAB', 'instrument': 'COS', 'derived_from': 'hst_cos_bpixtab_0251.rmap', 'reffile_switch': 'NONE', 'reffile_format': 'TABLE', 'rmap_relevance': 'ALWAYS', 'sha1sum': 'd2024dade52a406af70fcdf27a81088004d67cae'}),
     'parameters': ('DETECTOR', 'USEAFTER', 'REFERENCE'),
     'selections': [('FUV', '1996-10-01 00:00:00', 's7g1700dl_bpix.fits'),
                    ('FUV', '2009-05-11 00:00:00', 'z1r1943fl_bpix.fits'),
                    ('NUV', '1996-10-01 00:00:00', 's7g1700pl_bpix.fits'),
                    ('NUV', '2009-05-11 00:00:00', 'uas19356l_bpix.fits')],
     'text_descr': 'Data Quality (Bad Pixel) Initialization Table'}
    """
def test_rmap_tojson():
    """
    >>> r = rmap.get_cached_mapping("data/hst_cos_bpixtab_0252.rmap")
    >>> pp(r.tojson())
    '{"header": {"observatory": "hst", "name": "hst_cos_bpixtab_0252.rmap", "reffile_required": "none", "parkey": [["DETECTOR"], ["DATE-OBS", "TIME-OBS"]], "mapping": "reference", "filekind": "bpixtab", "instrument": "cos", "derived_from": "hst_cos_bpixtab_0251.rmap", "reffile_switch": "none", "reffile_format": "table", "rmap_relevance": "always", "sha1sum": "d2024dade52a406af70fcdf27a81088004d67cae"}, "selections": [["FUV", "1996-10-01 00:00:00", "s7g1700dl_bpix.fits"], ["FUV", "2009-05-11 00:00:00", "z1r1943fl_bpix.fits"], ["NUV", "1996-10-01 00:00:00", "s7g1700pl_bpix.fits"], ["NUV", "2009-05-11 00:00:00", "uas19356l_bpix.fits"]], "parameters": ["DETECTOR", "USEAFTER", "REFERENCE"], "text_descr": "Data Quality (Bad Pixel) Initialization Table"}'
    """

def test_load_rmap_bad_expr(self):
    """
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_badexpr.rmap")
    Traceback (most recent call last):
    ...
    SyntaxError: invalid syntax
    """

def test_rmap_get_parkey_map():
    """
    >>> i = rmap.get_cached_mapping("hst_acs.imap")
    >>> pp(i.get_parkey_map())
    {'APERTURE': ['*',
                  'WFC',
                  'WFC-FIX',
                  'WFC1',
                  'WFC1-1K',
                  'WFC1-2K',
                  'WFC1-512',
                  'WFC1-CTE',
                  'WFC1-FIX',
                  'WFC1-IRAMP',
                  'WFC1-IRAMPQ',
                  'WFC1-MRAMP',
                  'WFC1-MRAMPQ',
                  'WFC1-POL0UV',
                  'WFC1-POL0V',
                  'WFC1-POL120UV',
                  'WFC1-POL120V',
                  'WFC1-POL60UV',
                  'WFC1-POL60V',
                  'WFC1-SMFL',
                  'WFC2',
                  'WFC2-2K',
                  'WFC2-FIX',
                  'WFC2-MRAMP',
                  'WFC2-ORAMP',
                  'WFC2-ORAMPQ',
                  'WFC2-POL0UV',
                  'WFC2-POL0V',
                  'WFC2-POL120UV',
                  'WFC2-POL120V',
                  'WFC2-POL60UV',
                  'WFC2-POL60V',
                  'WFC2-SMFL',
                  'WFCENTER'],
     'ATODCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'BIASCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'CCDAMP': ['A', 'ABCD', 'AC', 'AD', 'B', 'BC', 'BD', 'C', 'D', 'N/A'],
     'CCDCHIP': ['N/A'],
     'CCDGAIN': ['0.5', '1.0', '1.4', '2.0', '4.0', '8.0', 'N/A'],
     'CRCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'DARKCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'DETECTOR': ['HRC', 'SBC', 'WFC'],
     'DQICORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'DRIZCORR': ['NONE', 'COMPLETE', 'PERFORM', 'OMIT', 'UNDEFINED'],
     'FILTER1': ['*',
                 'BLOCK1',
                 'BLOCK2',
                 'BLOCK3',
                 'BLOCK4',
                 'CLEAR1L',
                 'CLEAR1S',
                 'F115LP',
                 'F122M',
                 'F125LP',
                 'F140LP',
                 'F150LP',
                 'F165LP',
                 'F475W',
                 'F502N',
                 'F550M',
                 'F555W',
                 'F606W',
                 'F625W',
                 'F658N',
                 'F775W',
                 'F850LP',
                 'F892N',
                 'G800L',
                 'N/A',
                 'POL0UV',
                 'POL120UV',
                 'POL60UV',
                 'PR110L',
                 'PR130L'],
     'FILTER2': ['CLEAR2L',
                 'CLEAR2S',
                 'F220M',
                 'F220W',
                 'F250W',
                 'F330W',
                 'F344N',
                 'F410W',
                 'F435W',
                 'F660N',
                 'F814W',
                 'FR1016N',
                 'FR388N',
                 'FR423N',
                 'FR459M',
                 'FR462N',
                 'FR505N',
                 'FR551N',
                 'FR555N',
                 'FR601N',
                 'FR647M',
                 'FR656N',
                 'FR716N',
                 'FR782N',
                 'FR853N',
                 'FR914M',
                 'FR931N',
                 'N/A',
                 'POL0V',
                 'POL120V',
                 'POL60V',
                 'PR200L'],
     'FLASHCUR': ['HIGH', 'LOW', 'MED'],
     'FLATCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'FLSHCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'FW1OFFST': ['-1.0', '1.0', 'N/A'],
     'FW2OFFST': ['-1.0', '1.0', 'N/A'],
     'FWSOFFST': ['N/A'],
     'GLINCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'LTV1': ['-1816.0',
              '-2048.0',
              '-3072.0',
              '-3584.0',
              '-3604.0',
              '19.0',
              '22.0',
              '24.0',
              'N/A'],
     'LTV2': ['-1.0',
              '-1023.0',
              '-1535.0',
              '-1591.0',
              '-57.0',
              '-824.0',
              '0.0',
              '20.0',
              'N/A'],
     'NUMCOLS': ['1046.0',
                 '1062.0',
                 '2070.0',
                 '2300.0',
                 '4144.0',
                 '512.0',
                 '534.0',
                 'N/A'],
     'NUMROWS': ['1024.0', '1044.0', '2046.0', '2068.0', '400.0', '512.0', 'N/A'],
     'OBSTYPE': ['CORONAGRAPHIC', 'IMAGING', 'SPECTROSCOPIC'],
     'PCTECORR': ['NONE', 'COMPLETE', 'PERFORM', 'OMIT', 'UNDEFINED'],
     'PHOTCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'SHADCORR': ['PERFORM', 'NONE', 'OMIT', 'COMPLETE', 'UNDEFINED'],
     'SHUTRPOS': ['A', 'B'],
     'XCORNER': ['N/A'],
     'YCORNER': ['N/A']}
    """
    
    
def test_rmap_get_parkey_map():
    """
    >>> i = rmap.get_cached_mapping("hst_acs.imap")
    >>> i.get_rmap("foo")
    Traceback (most recent call last):
    ...
    CrdsUnknownReftypeError: Unknown reference type 'foo'
    """

def test_rmap_get_reference_parkeys():
    """
    >>> r = rmap.get_cached_mapping("data/jwst_miri_specwcs_0004.rmap")
    >>> r.parkey
    (('META.INSTRUMENT.DETECTOR', 'META.INSTRUMENT.CHANNEL', 'META.INSTRUMENT.BAND', 'META.SUBARRAY.NAME'),)
    >>> r.get_reference_parkeys()
    ('DETECTOR', 'CHANNEL', 'BAND', 'SUBARRAY', 'META.EXPOSURE.TYPE')
    """

def test_rmap_get_valid_values_map():
    """
    >>> i = rmap.get_cached_mapping("hst_acs.imap")
    >>> pp(i.get_valid_values_map())
    {'APERTURE': ['NONE',
                  'SBC',
                  'SBC-FIX',
                  'WFC',
                  'WFC-FIX',
                  'WFC1',
                  'WFC1-1K',
                  'WFC1-2K',
                  'WFC1-512',
                  'WFC1-CTE',
                  'WFC1-FIX',
                  'WFC1-IRAMP',
                  'WFC1-IRAMPQ',
                  'WFC1-MRAMP',
                  'WFC1-MRAMPQ',
                  'WFC1-POL0UV',
                  'WFC1-POL0V',
                  'WFC1-POL120UV',
                  'WFC1-POL120V',
                  'WFC1-POL60UV',
                  'WFC1-POL60V',
                  'WFC1-SMFL',
                  'WFC2',
                  'WFC2-2K',
                  'WFC2-FIX',
                  'WFC2-MRAMP',
                  'WFC2-ORAMP',
                  'WFC2-ORAMPQ',
                  'WFC2-POL0UV',
                  'WFC2-POL0V',
                  'WFC2-POL120UV',
                  'WFC2-POL120V',
                  'WFC2-POL60UV',
                  'WFC2-POL60V',
                  'WFC2-SMFL',
                  'WFCENTER'],
     'ATODCORR': [],
     'BIASCORR': [],
     'CCDAMP': ['A', 'ABCD', 'AC', 'AD', 'B', 'BC', 'BD', 'C', 'D'],
     'CCDCHIP': [],
     'CCDGAIN': ['0.5', '1.0', '1.4', '2.0', '4.0', '8.0'],
     'CRCORR': [],
     'DARKCORR': [],
     'DETECTOR': ['HRC', 'SBC', 'WFC'],
     'DQICORR': [],
     'DRIZCORR': [],
     'FILTER1': ['BLOCK1',
                 'BLOCK2',
                 'BLOCK3',
                 'BLOCK4',
                 'CLEAR1L',
                 'CLEAR1S',
                 'F115LP',
                 'F122M',
                 'F125LP',
                 'F140LP',
                 'F150LP',
                 'F165LP',
                 'F475W',
                 'F502N',
                 'F550M',
                 'F555W',
                 'F606W',
                 'F625W',
                 'F658N',
                 'F775W',
                 'F850LP',
                 'F892N',
                 'G800L',
                 'POL0UV',
                 'POL120UV',
                 'POL60UV',
                 'PR110L',
                 'PR130L'],
     'FILTER2': ['CLEAR2L',
                 'CLEAR2S',
                 'F220W',
                 'F250W',
                 'F330W',
                 'F344N',
                 'F435W',
                 'F660N',
                 'F814W',
                 'FR1016N',
                 'FR388N',
                 'FR423N',
                 'FR459M',
                 'FR462N',
                 'FR505N',
                 'FR551N',
                 'FR601N',
                 'FR647M',
                 'FR656N',
                 'FR716N',
                 'FR782N',
                 'FR853N',
                 'FR914M',
                 'FR931N',
                 'POL0V',
                 'POL120V',
                 'POL60V',
                 'PR200L'],
     'FLASHCUR': ['HIGH', 'LOW', 'MED'],
     'FLATCORR': [],
     'FLSHCORR': [],
     'FW1OFFST': ['-1', '0', '1', '2'],
     'FW2OFFST': ['-1', '0', '1', '2'],
     'FWSOFFST': ['-1', '0', '1', '2'],
     'GLINCORR': [],
     'LTV1': [],
     'LTV2': [],
     'NUMCOLS': [],
     'NUMROWS': [],
     'OBSTYPE': ['CORONAGRAPHIC', 'IMAGING', 'INTERNAL', 'SPECTROSCOPIC'],
     'PCTECORR': [],
     'PHOTCORR': [],
     'SHADCORR': [],
     'SHUTRPOS': ['A', 'B'],
     'XCORNER': [],
     'YCORNER': []}

    >>> pp(i.get_valid_values_map(remove_special=False)["CCDGAIN"])
    ['0.5', '1.0', '1.4', '2.0', '4.0', '8.0']

    >>> pp(i.get_valid_values_map(condition=True)["FW1OFFST"])
    ['-1.0', '0.0', '1.0', '2.0']

    """

def test_rmap_get_best_references_fail():
    """
    >>> i = rmap.get_cached_mapping("hst_acs.imap")
    >>> i.get_best_references({
    ... "DETECTOR" : "HRC",
    ... "CCDAMP" : "B",
    ... "CCDGAIN" : "7.0",
    ... "DARKCORR" : "PERFORM",
    ... "DATE-OBS" : "2015-04-30",
    ... "TIME-OBS" : "16:43:00",
    ... }, include=["darkfile"])
    {'darkfile': 'NOT FOUND No match found.'}
    """

def test_rmap_get_best_references_include():
    """
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_comment.rmap")
    >>> header = {
    ... 'CCDAMP': 'ABCD',
    ... 'CCDGAIN': '1.0',
    ... 'DARKCORR': 'UNDEFINED',
    ... 'DATE-OBS': '2002-07-18',
    ... 'DETECTOR': 'WFC',
    ... 'TIME-OBS': '18:09:15.773332'}
    >>> r.get_best_references(header, include=["flatfile"])
    Traceback (most recent call last):
    ...
    CrdsUnknownReftypeError: ReferenceMapping 'hst_acs_darkfile_comment.rmap' can only compute bestrefs for type 'darkfile' not ['flatfile']
    """

def test_validate_mapping_valid():
    """
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile.rmap")
    >>> r.validate_mapping()
    """

def test_validate_mapping_invalid1():
    """
    >>> log.set_test_mode()
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_invalid1.rmap")
    >>> r.validate_mapping()
    CRDS  : ERROR    Match('DETECTOR', 'CCDAMP', 'CCDGAIN') : ('HRC', 'A|ABCD|AD|B|BC|C|DDDD', '1.0|2.0|4.0|8.0') : '2002-03- 00:34:31' : UseAfter Invalid date/time format for ('DATE-OBS', 'TIME-OBS') value='2002-03- 00:34:31' exception is "Unknown numerical date format: '2002/03/ 00:34:31'"
    """

def test_validate_mapping_invalid2():
    """
    >>> log.set_test_mode()
    >>> r = rmap.get_cached_mapping("data/hst_acs_darkfile_invalid2.rmap")
    >>> r.validate_mapping()
    CRDS  : ERROR    Match('DETECTOR', 'CCDAMP', 'CCDGAIN') : ('FOOBAR', 'A|ABCD|AD|B|BC|C|DDDD', '1.0|2.0|4.0|8.0') :  parameter='DETECTOR' value='FOOBAR' is not in ('WFC', 'HRC', 'SBC')
    """

def test_rmap_asmapping_readonly():
    """
    >>> r = rmap.asmapping("data/hst_acs_darkfile.rmap", cached="readonly")
    """
    
# ==================================================================================

class TestRmap(CRDSTestCase):

    def test_get_imap_except(self):
        r = rmap.get_cached_mapping("hst.pmap")
        with self.assertRaises(exceptions.CrdsUnknownInstrumentError):
            r.get_imap("foo")

    def test_get_filekind(self):
        r = rmap.get_cached_mapping("hst.pmap")
        self.assertEqual(r.get_filekinds("data/j8bt05njq_raw.fits"),
                         [ 'PCTETAB', 'CRREJTAB', 'DARKFILE', 'D2IMFILE', 'BPIXTAB', 'ATODTAB', 'BIASFILE',
                           'SPOTTAB', 'MLINTAB', 'DGEOFILE', 'FLSHFILE', 'NPOLFILE', 'OSCNTAB', 'CCDTAB',
                           'SHADFILE', 'IDCTAB', 'IMPHTTAB', 'PFLTFILE', 'DRKCFILE', 'CFLTFILE', 'MDRIZTAB'])

    def test_get_equivalent_mapping(self):
        i = rmap.get_cached_mapping("data/hst_acs_0002.imap")
        self.assertEqual(i.get_equivalent_mapping("hst.pmap"), None)
        self.assertEqual(i.get_equivalent_mapping("data/hst_acs_0001.imap").name, "hst_acs.imap")
        self.assertEqual(i.get_equivalent_mapping("data/hst_acs_biasfile_0002.rmap").name, "hst_acs_biasfile.rmap")


    def test_list_references(self):
        self.assertEqual(rmap.list_references("*.r1h", "hst"), [])


# ==================================================================================


def tst():
    """Run module tests,  for now just doctests only."""
    import test_rmap, doctest
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRmap)
    unittest.TextTestRunner().run(suite)
    return doctest.testmod(test_rmap)

if __name__ == "__main__":
    print(tst())