import os
import tempfile
from uuid import uuid4
from decorify import no_print, redirect_stdout, redirect_stderr

def test_no_print(capsys):
    @no_print
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""

def test_redirect_stdout_file(capsys):
    with tempfile.TemporaryFile("w+") as f:
        @redirect_stdout(f)
        def print_hello():
            print("Hello, world!")
        
        print_hello()
        f.seek(0)
        assert f.read() == "Hello, world!\n"
        assert capsys.readouterr().out == ""

def test_redirect_stdout_str(capsys):
    filename = f"temp_{uuid4()}.txt"
    @redirect_stdout(filename)
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    with open(filename, "r") as f:
        assert f.read() == "Hello, world!\n"
    assert capsys.readouterr().out == ""
    os.remove(filename)

def test_redirect_stdout_none(capsys):
    @redirect_stdout()
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""