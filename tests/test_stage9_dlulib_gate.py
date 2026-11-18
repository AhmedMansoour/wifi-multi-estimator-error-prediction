import sys
from pathlib import Path
import zipfile
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jepformer.dlulib_gate import audit_archive


def test_only_lists_archive_without_opening_test_data(tmp_path):
    p=tmp_path/'example.zip'
    with zipfile.ZipFile(p,'w') as z:
        for floor in (1,2,3):
            for typ in (f'Training_DLULIB_Floor{floor}_All_20.xlsx',
                        f'Training_DLULIB_Floor{floor}_Mean.xlsx',
                        f'Testing_DLULIB_Floor{floor}.xlsx'):
                z.writestr(f'DLULIB_Floor_{floor}/{typ}',b'DUMMY NOT REAL XLSX')
    result=audit_archive(p,enforce_pinned_md5=False)
    assert result['expected_tables_present']
    assert not result['GT_accessed'] and not result['validation_completed']
    with pytest.raises(ValueError,match='MD5'):
        audit_archive(p,enforce_pinned_md5=True)


def test_missing_floor_is_exposed(tmp_path):
    p=tmp_path/'missing.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('DLULIB_Floor_1/Training_DLULIB_Floor1_All_20.xlsx','x')
    r=audit_archive(p,enforce_pinned_md5=False)
    assert not r['expected_tables_present']
    assert '3:test' in r['missing_or_ambiguous_roles']
