import configuration_service_client as conf_client

def test_basic_get():
    amqp_settings = conf_client.getSystemSettings('amqp')
    print amqp_settings
    assert amqp_settings is not None
    assert len(amqp_settings) > 0
    print 'test basic get passed'

def test_setAndDrop():
    system = 'test'
    settings = {'url': 'test'}
    conf_client.setSystemSettings(system, settings)
    received_settings = conf_client.getSystemSettings(system)
    assert received_settings == settings
    conf_client.dropSystemSettings(system)
    received_settings = conf_client.getSystemSettings(system)
    assert received_settings is None
    print 'test set and drop passed'

def test_invalidSet():
    valid_system_name = 'test'
    invalid_system_name = 1
    valid_settings = {'url': 'test'}
    invalid_settings = None
    # test invalid system name
    conf_client.setSystemSettings(invalid_system_name, valid_settings)
    received_settings = conf_client.getSystemSettings(invalid_system_name)
    assert received_settings is None
    # test invalid settings
    conf_client.setSystemSettings(valid_system_name, invalid_settings)
    received_settings = conf_client.getSystemSettings(valid_system_name)
    assert received_settings is None
    print 'test invalid set passed'

if __name__=='__main__':
    test_basic_get()
    test_setAndDrop()
    test_invalidSet()