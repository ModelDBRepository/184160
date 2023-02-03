'''
Defines a class, Neuron471087975, of neurons from Allen Brain Institute's model 471087975

A demo is available by running:

    python -i mosinit.py
'''
class Neuron471087975:
    def __init__(self, name="Neuron471087975", x=0, y=0, z=0):
        '''Instantiate Neuron471087975.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron471087975_instance is used instead
        '''
                
        self._name = name
        # load the morphology
        from load_swc import load_swc
        load_swc('Rorb-IRES2-Cre-D_Ai14_IVSCC_-168053.06.01.01_469628773_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon

        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron471087975_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im', u'K_P', u'K_T', u'Kv3_1', u'NaTs', u'Nap', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 40.56
            sec.e_pas = -90.7508341471
        for sec in self.apic:
            sec.cm = 2.46
            sec.g_pas = 0.000159058118123
        for sec in self.axon:
            sec.cm = 1.0
            sec.g_pas = 0.000485186159326
        for sec in self.dend:
            sec.cm = 2.46
            sec.g_pas = 1.21841366769e-05
        for sec in self.soma:
            sec.cm = 1.0
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Im = 5.39251e-05
            sec.gbar_Ih = 4.82595e-05
            sec.gbar_NaTs = 0.408145
            sec.gbar_Nap = 0.00037578
            sec.gbar_K_P = 0.0322045
            sec.gbar_K_T = 0.00163426
            sec.gbar_SK = 0.00474435
            sec.gbar_Kv3_1 = 0.183087
            sec.gbar_Ca_HVA = 0.000889089
            sec.gbar_Ca_LVA = 0.000315765
            sec.gamma_CaDynamics = 0.000426056
            sec.decay_CaDynamics = 930.258
            sec.g_pas = 0.000108847
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

