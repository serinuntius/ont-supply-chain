# supply chain

from boa.interop.System.Runtime import Log, GetTrigger, CheckWitness, Notify, Serialize, Deserialize
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.System.Blockchain import GetHeight, GetHeader
from boa.interop.System.Storage import GetContext, Get, Put, Delete



def Main(operation, args):
    if operation == 'Query':
        domain = args[0]
        return Query(domain)

    if operation == 'Register':
        domain = args[0]
        owner = args[1]
        return Register(domain, owner)

    if operation == 'Transfer':
        domain = args[0]
        to = args[1]
        return Transfer(domain, to)

    if operation == 'DeleteDomain':
        domain = args[0]
        return DeleteDomain(domain)

    
    if operation == 'RegisterUser':
        user_id = args[0]        
        position = args[1]  

        RegisterUser(user_id, position)


    if operation == 'RegisterItem':
        user_id = args[0]
        uuid = args[1]
        RegisterItem(user_id, uuid)

    return False


def Query(domain):
    return  Get(GetContext(), domain)

def Register(domain, owner):
    context = GetContext()
    occupy = Get(context, domain)
    if occupy != None:
        return False;
    Put(context, domain, owner)
    Notify('Register', domain, owner)

    return True

def RegisterUser(user_id, position):
    ctx = GetContext()

    Put(ctx, user_id, position)

def RegisterItem(user_id, _uuid):
    ctx = GetContext()
    timestamp = GetTime()

    user_possition = Get(ctx, user_id)

    if user_possition == None:
        Notify('user_possition is not found')
        return False

    # first idx
    uuid = _uuid + '-1'

    data = {
        'user_id': user_id,
        'uuid': uuid,
        'position': user_possition,
        'timestamp': timestamp,
    }

    serialized_data = Serialize(data)

    Put(ctx, uuid, data)

    return True

def Transfer(domain, to):
    if to == None:
        return False

    context = GetContext()
    owner = Get(context, domain)
    if owner == None:
        return False
    if owner == to:
        return True

    is_owner = CheckWitness(owner)

    if not is_owner:
        return False

    Put(context, domain, to)
    Notify('Transfer', domain)

    return True

def DeleteDomain(domain):
    context = GetContext()
    owner = Get(context, domain)
    is_owner = CheckWitness(owner)
    if not is_owner:
        return False

    Delete(context, domain)
    Notify('Delete', domain)

    return True