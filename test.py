from createStore import createStore
from combineReducers import combineReducers

def reducer1(action, state={'name': 'Kate', 'age': 22}):
    if action['type'] == 'INC':
        state['age'] += 1
        return state
    if action['type'] == 'DEC':
        state['age'] -= 1
        return state
    return state

store = createStore(reducer1)
print store.getState()

store.dispatch({'type': 'INC'})
print store.getState()

def listener1(t):
    print "listenr1",t

subscription = store.subscribe(lambda: listener1('xixi'))
store.dispatch({'type': 'INC'})
print store.getState()

subscription.unsubscribe()
store.dispatch({'type': 'INC'})
print store.getState()


def red2(action, state={'cate': 'workingExpe','years':0}):
    if action['type'] == 'INC':
        state['years'] += 1
        return state
    if action['type'] == 'DEC':
        state['years'] -= 1
        return state
    return state


rootReducer = combineReducers(reducer1, red2)

rootStore = createStore(rootReducer)

print rootStore.getState()

rootStore.dispatch({'type': 'INC'})
print rootStore.getState()
