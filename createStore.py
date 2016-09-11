from __future__ import print_function
import warnings

def createStore(reducer, initState=None, enhancer=None):
    if not callable(reducer):
        raise Exception("reducer must be a function")

    __ACTION = {'type': '@@INIT'}
   
    #initState has a higher priority, if both initState and reducer's own initState is provided, use initState
    curentState = initState or reducer(__ACTION)
    if curentState is None:
        raise Exception("either provide initState when invoke createStore or provide one to your reducer")

    if enhancer:
        if not callabel(enhancer):
            raise Exception("enhancer must be a function")
        enhancer(createStore)(reducer, initState)

    class Store(object):
        def __init__(self, __curentState):
            self.__curentState = curentState
            self.reducer = reducer
            self.listeners = []
            self.isSubscribed = False
            self.isDispatching = False

        def dispatch(self, action):
            """set curentState, invoke every listener func in listeners list"""
            if not isinstance(action, dict):
                raise Exception("action must be dict type")
            if not (action['type']):
                raise Exception("action must have a key called 'type'")
            #in case there are some async opeartion
            try:
                if self.isDispatching:
                    raise Exception("store is in the process of dispatching, your latest action may not be dispatched")
                else:
                    self.isDispatching = True
                    self.__curentState = self.reducer(action, self.__curentState)
            except Exception as ex:
                warnings.warn(ex.message, RuntimeWarning)
            finally:
                self.isDispatching = False

            if (self.listeners and self.isSubscribed):
                for i in self.listeners:
                    i()
            return action

        def getState(self):
            return self.__curentState

        def subscribe(self, listener):
            """listener is the function gets invoked everytime store dispatches an action"""
            if not callable(listener):
                raise Exception("listener must be a function")
            self.listeners.append(listener)
            self.isSubscribed = True
            listenerIndex = self.listeners.index(listener)

            class Unsubscriber(object):
                def __init__(self, store, index):
                    self.store = store
                    self.index = index
                def unsubscribe(self):
                    if not self.store.isSubscribed:
                        return
                    self.store.listeners.pop(self.index)
                    if not self.store.listeners:
                        self.store.isSubscribed = False
                    self.__del__()
                def __del__(self):
                    del self

            return Unsubscriber(self, listenerIndex)

        def replaceReducer(self, newReducer):
            """replace curent reducer with newReducer"""
            if not callable(newReducer):
                raise Exception("reducer must be a function")
            self.__curentState = curentState or newReducer(__ACTION)

    return Store(curentState)
