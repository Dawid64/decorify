import os
import sys
import tempfile
from uuid import uuid4
from decorify import mute, redirect


def test_mute_print(capsys):
    @mute
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"


def test_mute_all(capsys):
    @mute(mute_all=True)
    def print_hello():
        sys.stdout.write("Hello, world!\n")
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"
    sys.stdout.write("Hello, world!\n")
    assert capsys.readouterr().out == "Hello, world!\n"


def test_redirect_stdout_file(capsys):
    with tempfile.TemporaryFile("w+") as f:
        @redirect(stdout_target=f)
        def print_hello():
            print("Hello, world!")
        
        print_hello()
        f.seek(0)
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
    @redirect()
    def print_hello():
        print("Hello, world!")
    
    print_hello()
    assert capsys.readouterr().out == ""
    print("Hello, world!")
    assert capsys.readouterr().out == "Hello, world!\n"

def test_redirect_stderr_file(capsys):
    with tempfile.TemporaryFile("w+") as f:
        @redirect(stderr_target=f)
        def print_hello():
            print("Hello, world!", file=sys.stderr)
        
        print_hello()
        f.seek(0)
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
    @redirect()
    def print_hello():
        print("Hello, world!", file=sys.stderr)
    
    print_hello()
    assert capsys.readouterr().err == ""