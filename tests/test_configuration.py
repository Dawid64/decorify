from decorify.configuration import configure
import tempfile
from pytest import raises



def test_toml():
    # TODO toml is insalled on the system
    import toml
    data = {
        'age': 10,
        'name':"Piotrek"
    }

    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False, mode='w') as temp_file:
        toml.dump(data, temp_file)  # Write TOML data to the file
        temp_file_path = temp_file.name  # Store the path of the file

    dictconfig = configure(temp_file_path,logger=None)

    @dictconfig
    def who_am_i(age:int, name:str, letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    


    assert who_am_i(20, "Tomek") == "I'm Tomek and I have 20 years! a"
    assert who_am_i() == "I'm Piotrek and I have 10 years! a"
    assert who_am_i(20, letter='b') == "I'm Piotrek and I have 20 years! b"


def test_txt():
    data = {
        'age': 10,
        'name':"Piotrek"
    }

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode='w') as temp_file:
        temp_file.write(str(data)) # Write TOML data to the file
        temp_file_path = temp_file.name  # Store the path of the file

    dictconfig = configure(temp_file_path,logger=None)

    @dictconfig
    def who_am_i(age:int, name:str, letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    


    assert who_am_i(20, "Tomek") == "I'm Tomek and I have 20 years! a"
    assert who_am_i() == "I'm Piotrek and I have 10 years! a"
    assert who_am_i(20, letter='b') == "I'm Piotrek and I have 20 years! b"


def test_json():
    import json
    data = {
        'age': 10,
        'name':"Piotrek"
    }

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as temp_file:
        json.dump(data, temp_file)  # Write TOML data to the file
        temp_file_path = temp_file.name  # Store the path of the file

    dictconfig = configure(temp_file_path,logger=None)

    @dictconfig
    def who_am_i(age:int, name:str, letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    


    assert who_am_i(20, "Tomek") == "I'm Tomek and I have 20 years! a"
    assert who_am_i() == "I'm Piotrek and I have 10 years! a"
    assert who_am_i(20, letter='b') == "I'm Piotrek and I have 20 years! b"

def test_dict():
    data = {
        'age': 10,
        'name':"Piotrek"
    }



    dictconfig = configure(data,logger=None)

    @dictconfig
    def who_am_i(age:int, name:str, letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    


    assert who_am_i(20, "Tomek") == "I'm Tomek and I have 20 years! a"
    assert who_am_i() == "I'm Piotrek and I have 10 years! a"
    assert who_am_i(20, letter='b') == "I'm Piotrek and I have 20 years! b"

def test_exceptions_dict():
    data = {
        'age': 10,
        'name':"Piotrek"
    }


    dictconfig = configure(data,logger=None)
    @dictconfig
    def who_am_i(age:int, name:str, letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    
    with raises(ValueError):
        who_am_i(20.1)


    with raises(ValueError):
        who_am_i(name=20)
    assert who_am_i(name="Tomek") == "I'm Tomek and I have 10 years! a"
    

    data = {
        'age': 10,
        'name': 'Piotrek',
    }

    dictconfig = configure(data,logger=None)
    @dictconfig
    def who_am_i(age, name:str='None', letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    

    assert who_am_i('hundred',letter='b') == "I'm Piotrek and I have hundred years! b"
    assert who_am_i('hundred',"Tomek") == "I'm Tomek and I have hundred years! a"

    data = {
        'age': 10,
    }

    dictconfig = configure(data,logger=None)
    @dictconfig
    def who_am_i(age, name:str='None', letter:str='a'):
        return f"I'm {name} and I have {age} years! {letter}"
    
    
    assert who_am_i('hundred',letter='b') == "I'm None and I have hundred years! b"
    assert who_am_i('hundred',"Tomek") == "I'm Tomek and I have hundred years! a"
    with raises(ValueError):
        who_am_i(letter=3)











