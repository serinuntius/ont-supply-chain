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

        return RegisterUser(user_id, position)


    if operation == 'RegisterItem':
        user_id = args[0]
        ont_id = args[1]
        uuid = args[2]

        return RegisterItem(user_id, ont_id, uuid)

    if operation == 'GetPosition':
        user_id = args[0]

        return GetPosition(user_id)

    if operation == 'GetItem':
        uuid = args[0]
        return GetItem(uuid)

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

    return True

def GetPosition(user_id):
    ctx = GetContext()
    position = Get(ctx, user_id)
    Notify(['position', position])
    return True

def GetItem(uuid):
    ctx = GetContext()
    item = Get(ctx, uuid)
    if item == None:
        Notify('not found item')
        return False

    item = Deserialize(item)
    #Notify(['Item', item['user_id'], item['ont_id'], item['position'], item['timestamp']])

    Notify(['Item', item['user_id'], item['ont_id'], item['position'], item['timestamp']])
    return item['user_id'], item['ont_id'], item['position'], item['timestamp']]

def RegisterItem(user_id,ont_id, _uuid):
    ctx = GetContext()
    timestamp = GetTime()

    user_possition = Get(ctx, user_id)

    if user_possition == None:
        Notify('user_possition is not found')
        return False

    # first idx
   #  uuid = _uuid + '-1'

    data = {
        'user_id': user_id,
        'uuid': _uuid,
        'ont_id': ont_id,
        'position': user_possition,
        'timestamp': timestamp
    }

    # Deserialize
    serialized_data = Serialize(data)
    Notify(['serialized_data', serialized_data])

    Put(ctx, _uuid, serialized_data)

    return True

def  Transfer(domain, to):
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

def  DeleteDomain(domain):
    context = GetContext()
    owner = Get(context, domain)
    is_owner = CheckWitness(owner)
    if not is_owner:
        return False

    Delete(context, domain)
    Notify('Delete', domain)

    return True
