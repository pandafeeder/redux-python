from __future__ import print_function

def combineReducers(*reducers, **keyReducers):
    """
       returns a root reducer function, keys of the state returned by this root 
       reducer function is sub-reducer's name or supplied key word argu's key and
       value is value returned by sub-reducers
    """
    if reducers and keyReducers:
        raise Exception("don't provid reducers in both list and dict")

    reducerList = reducers or keyReducers.values()

    for i in reducerList:
        if not callable(i):
            raise Exception("reducer must be function")

    stateTree = {}

    if reducers:
        for i in reducers:
            stateTree.update({i.__name__: i})

    if keyReducers:
        for k,v in keyReducers.iteritems():
            stateTree.update({k: v})

    def rootReducer(action, state=stateTree):
        newStateTree = {}
        for k,v in stateTree.iteritems():
            newStateTree.update({k: v(action)})
        return newStateTree

    return rootReducer
