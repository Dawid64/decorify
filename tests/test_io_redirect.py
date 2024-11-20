from decorify import no_print

def test_no_print(capsys):
    @no_print
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""