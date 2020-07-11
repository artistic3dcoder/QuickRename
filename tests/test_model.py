from pytest import fixture

ROW = 0
COL = 1
NAME = "test_name"
DEST = "dummy_dest"
SRC = "dummy_src"


@fixture
def get_rename():
    """Instantiate RenameItem."""
    from quick_rename.models.model import RenameItem
    return RenameItem(col=COL, row=ROW, name=NAME, src=SRC, dest=DEST)


@fixture
def get_preprocessed():
    """Instantiate PreProcessed"""
    from quick_rename.models.model import PreProcessed
    return PreProcessed()


@fixture
def get_temp():
    """Get a temp file."""
    from tempfile import TemporaryFile
    return TemporaryFile()


@fixture
def add_preprocessed(get_preprocessed, get_temp):
    """Add an item to preprocessed."""
    from tempfile import gettempdir
    from os.path import basename
    f = get_temp
    pre = get_preprocessed
    pre.add_item(item=basename(f.name), directory=gettempdir())
    return pre, f


def remove_temp(f=None):
    """Remove temporary file."""
    from os import remove
    remove(f.name)


def test_rename_is_inst(get_rename):
    """Test that our RenameItem instantiates."""
    from quick_rename.models.model import RenameItem
    item = get_rename
    assert isinstance(item, RenameItem)


def test_rename_values(get_rename):
    """Test that the data we put in is the same data that we get out."""
    item = get_rename
    assert all(
        [item.col == COL, item.row == ROW, item.name == NAME, item.src == SRC, item.dest == DEST])


def test_preprocessed_is_inst(get_preprocessed):
    """Test that our PreProcessed instantiates."""
    from quick_rename.models.model import PreProcessed
    assert(get_preprocessed, PreProcessed)


def test_failure_to_add_item_to_preprocessed(get_preprocessed):
    """Test that we can add an item to PreProcessed."""
    assert not get_preprocessed.add_item(item="test_item", directory="/bad_dir")


def test_success_to_add_item_to_preprocessed(get_preprocessed):
    """Test that we can add an item to PreProcessed."""
    from tempfile import gettempdir, TemporaryFile
    from os.path import basename
    f = TemporaryFile()
    assert get_preprocessed.add_item(item=basename(f.name), directory=gettempdir())
    remove_temp(f)


def test_preprocessed_had_data(add_preprocessed):
    """Test that after adding an item to PreProcessed the internal count reflects this."""
    pre, f = add_preprocessed
    assert pre.count() == 1
    remove_temp(f)


def test_preprocessed_clear_data(add_preprocessed):
    """Test that after adding an item to PreProcessed the data can be cleared and the internal count reflects this."""
    pre, f = add_preprocessed
    pre.clear()
    assert pre.count() == 0
    remove_temp(f)


def test_preprocessed_data(add_preprocessed):
    """Test that after adding an item to PreProcessed the data can be cleared and the internal count reflects this."""
    from quick_rename.models.model import PreProcessedData
    pre, f = add_preprocessed
    assert len(pre.data) == 1 and isinstance(pre.data[0], PreProcessedData)
    remove_temp(f)
