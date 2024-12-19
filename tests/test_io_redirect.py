import os
import sys
from uuid import uuid4
from pytest import raises
from decorify import mute, redirect


class TempFile:
    def __init__(self):
        self.text = ""
    
    def write(self, text):
        self.text += text
        
    def read(self):
        return self.text


def test_mute_print(capsys):
    @mute(level="print")
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"


def test_mute_stdout(capsys):
    @mute(level="stdout")
    def print_hello():
        print("Hello, world!")
        sys.stdout.write("Hello, world!\n")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"
    sys.stdout.write("Hello, world!\n")


def test_mute_warning_without_error(capsys):
    @mute(level="warning")
    def print_hello():
        print("Hello, world!", file=sys.stderr)
    
    print_hello()
    assert capsys.readouterr().err == ""
    print("Hello, world!", file=sys.stderr)
    assert capsys.readouterr().err == "Hello, world!\n"


def test_redirect_stdout_file(capsys):
    f = TempFile()
    @redirect(stdout_target=f)
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert f.read() == "Hello, world!\n"
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"

def test_redirect_stdout_str(capsys):
    filename = f"temp_{uuid4()}.txt"
    @redirect(stdout_target=filename)
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    with open(filename, "r") as f:
        assert f.read() == "Hello, world!\n"
    assert capsys.readouterr().out == ""
    os.remove(filename)
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"

def test_redirect_stdout_none(capsys):
    @redirect(stdout_target=None)
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"

def test_redirect_stderr_file(capsys):
    f = TempFile()
    @redirect(stderr_target=f)
    def print_hello():
        print("Hello, world!", file=sys.stderr)
    
    print_hello()
    assert f.read() == "Hello, world!\n"
    assert capsys.readouterr().err == ""

def test_redirect_stderr_str(capsys):
    filename = f"temp_{uuid4()}.txt"
    @redirect(stderr_target=filename)
    def print_hello():
        print("Hello, world!", file=sys.stderr)
    
    print_hello()
    try:
        with open(filename, "r") as f:
            assert f.read() == "Hello, world!\n"
        assert capsys.readouterr().err == ""
    finally:
        os.remove(filename)

def test_redirect_stderr_none(capsys):
    @redirect(stderr_target=None)
    def print_hello():
        print("Hello, world!", file=sys.stderr)
    
    print_hello()
    assert capsys.readouterr().err == ""
    
    
def test_redirect_incorrect_stdout():
    with raises(ValueError):
        @redirect(stdout_target=1)
        def print_hello():
            print("Hello, world!")
            
        print_hello()
            

def test_redirect_incorrect_stderr():
    with raises(ValueError):
        @redirect(stderr_target=1)
        def print_hello():
            print("Hello, world!")
        
        print_hello()