from amuse.legacy import *
from amuse.legacy.interface.gd import GravitationalDynamics
from amuse.legacy.interface.gd import NBodyGravitationalDynamicsBinding
from amuse.legacy.interface.gd import GravitationalDynamicsInterface
from amuse.legacy.support.lit import LiteratureRefs
from amuse.support.data.core import Particles,ParticlesWithUnitsConverted
from amuse.support.data import binding


class BHTreeInterface(LegacyInterface, LiteratureRefs, GravitationalDynamics):
    """
        .. [#] Barnes, J., Hut, P., A Hierarchical O(N log N) force-calculation algorithm, *Nature*, **4**, 324 (1986)   
    """
    include_headers = ['BHTree_code.h', 'parameters.h', 'local.h']
    
    timestep = legacy_global(name='timestep',id=21,dtype='d')
    eps2_for_gravity = legacy_global(name='eps2_for_gravity',id=22,dtype='d')
    theta_for_tree = legacy_global(name='theta_for_tree',id=23,dtype='d')
    
    use_self_gravity = legacy_global(name='use_self_gravity',id=24,dtype='i')
    ncrit_for_tree = legacy_global(name='ncrit_for_tree',id=25,dtype='i')
    
    dt_dia = legacy_global(name='dt_dia',id=246,dtype='d')

    def __init__(self, convert_nbody = None, **kwargs):
        LegacyInterface.__init__(self, name_of_the_worker="worker_code", **kwargs)
        """
        self.parameters = parameters.Parameters(self.parameter_definitions, self)
        if convert_nbody is None:
            convert_nbody = nbody_system.nbody_to_si.get_default()
            
        self.convert_nbody = convert_nbody
        """
        LiteratureRefs.__init__(self)

    @legacy_function   
    def setup_module():
        function = LegacyFunctionSpecification() 
        function.result_type = 'i'
        return function
   
    @legacy_function      
    def cleanup_module():
        function = LegacyFunctionSpecification()  
        function.result_type = 'i'
        return function
    
    @legacy_function    
    def initialize_particles():
        function = LegacyFunctionSpecification() 
        function.addParameter('time', dtype='d', direction=function.IN)
        function.result_type = 'i'
        return function;
       
    @legacy_function  
    def reinitialize_particles():
        function = LegacyFunctionSpecification()  
        function.result_type = 'i'
        return function
       
class BHTree(GravitationalDynamicsInterface):
    
    
    def __init__(self, convert_nbody = None):
        
        if convert_nbody is None:
            convert_nbody = nbody_system.nbody_to_si.get_default()
       
        
        legacy_interface = BHTreeInterface()
        
        GravitationalDynamicsInterface.__init__(
            self,
            legacy_interface,
            convert_nbody,
        )     
            
    def setup_parameters(self, object):
        object.add_attribute_parameter(
            "eps2_for_gravity",
            "epsilon_squared", 
            "smoothing parameter for gravity calculations", 
            nbody_system.length * nbody_system.length, 
            0.3 | nbody_system.length * nbody_system.length
        )
        object.add_attribute_parameter(
            "timestep",
            "timestep", 
            "constant timestep for iteration", 
            nbody_system.time, 
            0.7 | nbody_system.time
        )
        object.add_attribute_parameter(
            "theta_for_tree",
            "openings_angle", 
            "openings angle for building the tree between 0 and 1", 
            units.none,
            0.5 | units.none
        )
        
    def setup_methods(self, object):
        GravitationalDynamicsInterface.setup_methods(self, object)
        
        object.add_method(
            "new_particle", 
            (
                nbody_system.mass,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.speed,
                nbody_system.speed,
                nbody_system.speed,
            ), 
            ( 
                object.NO_UNIT,
                object.ERROR_CODE
            )
        )
        object.add_method(
            "delete_particle", 
            (
                object.NO_UNIT,
            ), 
            ( 
                object.ERROR_CODE,
            )
        )
        object.add_method(
            "get_state", 
            (
                object.NO_UNIT,
            ), 
            (
                nbody_system.mass,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.speed,
                nbody_system.speed,
                nbody_system.speed,
                object.ERROR_CODE
            )
        )
        object.add_method(
            "set_state", 
            (
                object.NO_UNIT,
                nbody_system.mass,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                nbody_system.speed,
                nbody_system.speed,
                nbody_system.speed,
            ), 
            (
                object.ERROR_CODE
            )
        )
        object.add_method(
            "set_mass", 
            (
                object.NO_UNIT,
                nbody_system.mass,
            ), 
            (
                object.ERROR_CODE
            )
        )
        object.add_method(
            "get_mass", 
            (
                object.NO_UNIT,
            ), 
            (
                nbody_system.mass,
                object.ERROR_CODE
            )
        )
        object.add_method(
            "set_radius", 
            (
                object.NO_UNIT,
                nbody_system.length,
            ), 
            (
                object.ERROR_CODE
            )
        )
        object.add_method(
            "get_radius", 
            (
                object.NO_UNIT,
            ), 
            (
                nbody_system.length,
                object.ERROR_CODE
            )
        )
        object.add_method(
            "set_position", 
            (
                object.NO_UNIT,
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
            ), 
            (
                object.ERROR_CODE
            )
        )
        object.add_method(
            "get_position", 
            (
                object.NO_UNIT,
            ), 
            (
                nbody_system.length,
                nbody_system.length,
                nbody_system.length,
                object.ERROR_CODE
            )
        )
    
    def setup_all_particles(self, object):
        object.define_set('particles', 'index_of_the_particle')
        object.set_new('particles', 'new_particle')
        object.set_delete('particles', 'delete_particle')
        object.add_setter('particles', 'set_state')
        object.add_getter('particles', 'get_state')
        object.add_setter('particles', 'set_mass')
        object.add_getter('particles', 'get_mass', names = ('mass',))
        object.add_setter('particles', 'set_position')
        object.add_getter('particles', 'get_position')
    
