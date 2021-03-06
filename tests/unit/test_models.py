import frontmatter
import responses

from archivy.extensions import get_max_id

attributes = ["type", "title", "desc", "tags", "path", "id"]


def test_new_note(test_app, note_fixture):
    """
    Check that a new note is correctly saved into the filesystem
    with the right attributes and the right id.
    """

    with test_app.app_context():
        max_id = get_max_id()
        assert note_fixture.id == max_id

    saved_file = frontmatter.load(note_fixture.fullpath)
    for attr in attributes:
        assert getattr(note_fixture, attr) == saved_file[attr]

def test_bookmark_sanitization(test_app, client, mocked_responses, bookmark_fixture):
    """Tests bookmark contents are correctly saved and converted to proper Markdown"""

    with test_app.app_context():
        assert bookmark_fixture.id == get_max_id()

    saved_file = frontmatter.load(bookmark_fixture.fullpath)
    for attr in attributes:
        assert getattr(bookmark_fixture, attr) == saved_file[attr]
    assert bookmark_fixture.url == saved_file["url"] 

    # remove buggy newlines that interfere with checks:
    bookmark_fixture.content = bookmark_fixture.content.replace("\n", "")
    # test script is sanitized 
    assert bookmark_fixture.content.find("<script>") == -1
    # test relative urls in the HTML are remapped to an absolute urls
    assert bookmark_fixture.content.find("example.com/images/image1.png") != -1
    assert bookmark_fixture.content.find("example.com/testing-absolute-url") != -1
    


