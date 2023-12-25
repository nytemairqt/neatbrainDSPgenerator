#------------------------------------------------------------------------------------
# NODES
#------------------------------------------------------------------------------------

def open_chain(name, chain_type, folded=0, extra_props=None):
	chain = []
	chain.append(f'<!-- Begin Chain {name} -->')
	chain.append(f'<Node ID="{name}" FactoryPath="{chain_type}" Bypassed="0" Folded="{folded}">') # container.chain, container.split
	if extra_props != None:
		chain.append(f'<Properties>')
		for prop in extra_props:
			chain.append(prop)
		chain.append(f'</Properties>')
	chain.append(f'<Nodes>')	

	return chain

def close_chain(name, extra_params=None):
	chain = []
	chain.append(f'</Nodes>')
	chain.append(f'<Parameters>')
	chain.append(f'</Parameters>')
	chain.append(f'</Node>')
	chain.append(f'<!-- End Chain {name} -->')
	return chain

def open_cloner(name):
	cloner = []
	cloner.append(f'<!-- Begin Cloner Object {name} -->')
	cloner.append(f'<Node ID="{name}" FactoryPath="container.clone" Bypassed="0" ShowClones="1" ShowParameters="1">')
	cloner.append(f'<Properties>')
	cloner.append(f'<Property ID="IsVertical" Value="0"/>')
	cloner.append(f'</Properties>')
	cloner.append(f'<Nodes>')	
	return cloner 

def close_cloner(name, num_clones):
	cloner = []
	cloner.append(f'</Nodes>')
	cloner.append(f'<Parameters>')
	cloner.append(f'<Parameter MinValue="1.0" MaxValue="{num_clones}" StepSize="1.0" ID="NumClones" Value="{num_clones}"/>')
	cloner.append(f'<Parameter MinValue="0.0" MaxValue="2.0" StepSize="1.0" ID="SplitSignal" Value="1.0"/>') # Splitter Mode
	cloner.append(f'</Parameters>')
	cloner.append(f'</Node>')
	cloner.append(f'<!-- End Cloner Object {name} -->')
	return cloner

def add_clone_sliderpack(name, num_sliders):
	sliderpack = []
	sliderpack.append(f'<Node ID="container_{name}" FactoryPath="container.no_midi" Bypassed="0">')
	sliderpack.append(f'<Nodes>')
	sliderpack.append(f'<Node ID="sliderpack_{name}" FactoryPath="control.clone_pack" Bypassed="0">')
	sliderpack.append(f'<ModulationTargets>')
	sliderpack.append(f'</ModulationTargets>')
	sliderpack.append(f'<ComplexData>')
	sliderpack.append(f'<SliderPacks>')
	sliderpack.append(f'</SliderPacks>')
	sliderpack.append(f'</ComplexData>')
	sliderpack.append(f'<Parameters>')
	sliderpack.append(f'<Parameter MinValue="1.0" MaxValue="{num_sliders}" StepSize="1.0" ID="NumClones" Value="{num_sliders}"/>')
	sliderpack.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	sliderpack.append(f'</Parameters>')
	sliderpack.append(f'</Node>')
	sliderpack.append(f'</Nodes>')
	sliderpack.append(f'<Parameters/>')
	sliderpack.append(f'</Node>')
	return sliderpack 

def add_clone_cable(name, num_clones, value=1.0, mode="Fixed", use_container=True):
	cable = []
	if (use_container):
		cable.append(f'<Node ID="container_{name}" FactoryPath="container.no_midi" Bypassed="0">')
		cable.append(f'<Nodes>')
	cable.append(f'<Node ID="cable_{name}" FactoryPath="control.clone_cable" Bypassed="0">')
	cable.append(f'<Properties>')
	cable.append(f'<Property ID="Mode" Value="{mode}"/>')
	cable.append(f'</Properties>')
	cable.append(f'<Parameters>')
	cable.append(f'<Parameter MinValue="1.0" MaxValue="40.0" StepSize="1.0" ID="NumClones" Value="{num_clones}"/>')
	cable.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="{value}"/>')
	cable.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Gamma" Value="0.0"/>')
	cable.append(f'</Parameters>')
	cable.append(f'<ModulationTargets>')
	cable.append(f'</ModulationTargets>')
	cable.append(f'</Node>')
	if use_container:
		cable.append(f'</Nodes>')
		cable.append(f'<Parameters/>')
		cable.append(f'</Node>')
	return cable 

def add_sine(name, freq_ratio):
	sine = []
	sine.append(f'<!-- Oscillator {name} -->')
	sine.append(f'<Node ID="{name}" FactoryPath="core.oscillator" Bypassed="0">')
	sine.append(f'<ComplexData>')
	sine.append(f'<DisplayBuffers>')
	sine.append(f'<DisplayBuffer Index="-1"/>')
	sine.append(f'</DisplayBuffers>')
	sine.append(f'</ComplexData>')
	sine.append(f'<Parameters>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="4.0" StepSize="1.0" ID="Mode" Automated="1"/>')
	sine.append(f'<Parameter MinValue="20.0" MaxValue="20000.0" StepSize="0.1000000014901161" SkewFactor="0.2299045622348785" ID="Frequency" Value="220.0"/>')
	sine.append(f'<Parameter MinValue="1.0" MaxValue="30.0" StepSize="1.0" ID="Freq Ratio" Value="{freq_ratio}"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Gate" Value="1.0"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Phase" Value="0.0"/>')
	sine.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Gain" Value="1.0"/>')
	sine.append(f'</Parameters>')
	sine.append(f'</Node>')
	sine.append(f'<!-- End Oscillator -->')
	return sine

def add_AHDSR(name, attack, attack_level, decay, sustain, release, folded=0, skew=1.0, a_max=10000, d_max=40000, r_max=40000):
	ahdsr = []
	ahdsr.append(f'<!-- AHDSR {name} -->')
	ahdsr.append(f'<Node ID="{name}" FactoryPath="envelope.ahdsr" Bypassed="0" Folded="{folded}">')
	ahdsr.append(f'<Properties>')
	ahdsr.append(f'<Property ID="NumParameters" Value="2"/>')
	ahdsr.append(f'</Properties>')
	ahdsr.append(f'<SwitchTargets>')
	ahdsr.append(f'<SwitchTarget>')
	ahdsr.append(f'<Connections> <!-- CV -->')
	ahdsr.append(f'</Connections>')
	ahdsr.append(f'</SwitchTarget>')
	ahdsr.append(f'<SwitchTarget>')
	ahdsr.append(f'<Connections> <!-- GT -->')
	ahdsr.append(f'</Connections>')
	ahdsr.append(f'</SwitchTarget>')
	ahdsr.append(f'</SwitchTargets>')
	ahdsr.append(f'<ComplexData>')
	ahdsr.append(f'<DisplayBuffers>')
	ahdsr.append(f'<DisplayBuffer Index="-1" EmbeddedData=""/>')
	ahdsr.append(f'</DisplayBuffers>')
	ahdsr.append(f'</ComplexData>')
	ahdsr.append(f'<Parameters>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="{a_max}" StepSize="0.1000000014901161" SkewFactor="{skew}" ID="Attack" Value="{attack}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="AttackLevel" Value="{attack_level}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="10000.0" StepSize="0.1000000014901161" SkewFactor="{skew}" ID="Hold" Value="20.0"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="{d_max}" StepSize="0.1000000014901161" SkewFactor="{skew}" ID="Decay" Value="{decay}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Sustain" Value="{sustain}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="{r_max}" StepSize="0.1000000014901161" SkewFactor="{skew}" ID="Release" Value="{release}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="AttackCurve" Value="0.5"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Retrigger" Value="0.0"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Gate" Value="0.0"/>')
	ahdsr.append(f'</Parameters>')
	ahdsr.append(f'</Node> <!-- End AHDSR -->')
	return ahdsr 

def add_filter(name, frequency):
	lowpassFilter = []
	lowpassFilter.append(f'<Node ID="{name}" FactoryPath="filters.one_pole" Bypassed="0">')
	lowpassFilter.append(f'<ComplexData>')
	lowpassFilter.append(f'<Filters>')
	lowpassFilter.append(f'<Filter Index="-1" EmbeddedData=""/>')
	lowpassFilter.append(f'</Filters>')
	lowpassFilter.append(f'</ComplexData>')
	lowpassFilter.append(f'<Parameters>')
	lowpassFilter.append(f'<Parameter MinValue="20.0" MaxValue="20000.0" SkewFactor="0.2299045622348785"')
	lowpassFilter.append(f'ID="Frequency" Value="{frequency}"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.300000011920929" MaxValue="9.899999618530273" SkewFactor="0.2647178173065186"')
	lowpassFilter.append(f'ID="Q" Value="1.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="-18.0" MaxValue="18.0" ID="Gain" Value="0.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" SkewFactor="0.3010300099849701"')
	lowpassFilter.append(f'ID="Smoothing" Value="0.009999999776482582"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Mode" Value="0.0"/>')
	lowpassFilter.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Enabled" Value="1.0"/>')
	lowpassFilter.append(f'</Parameters>')
	lowpassFilter.append(f'</Node>')
	return lowpassFilter

def add_gain(name, invert=False):
	gain = []
	gain.append(f'<Node ID="{name}" FactoryPath="core.gain" Bypassed="0">')
	gain.append(f'<Parameters>')
	if invert:
		gain.append(f'<Parameter MinValue="0" MaxValue="-100" StepSize="0.1000000014901161" SkewFactor="5.422270774841309" ID="Gain" Value="0.0"/>')
	else:
		gain.append(f'<Parameter MinValue="-100" MaxValue="0" StepSize="0.1000000014901161" SkewFactor="5.422270774841309" ID="Gain" Value="0.0"/>')
	gain.append(f'<Parameter MinValue="0.0" MaxValue="1000.0" StepSize="0.1000000014901161" SkewFactor="0.3010300099849701" ID="Smoothing" Value="20.0"/>')
	gain.append(f'<Parameter MinValue="-100.0" MaxValue="0.0" StepSize="0.1000000014901161" SkewFactor="5.422270774841309" ID="ResetValue" Value="0.0"/>')
	gain.append(f'</Parameters>')
	gain.append(f'</Node>')
	return gain

def add_voice_manager(name):
	voice_manager = []
	voice_manager.append(f'<Node ID="{name}" FactoryPath="envelope.voice_manager" Bypassed="0">')
	voice_manager.append(f'<Parameters>')
	voice_manager.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Kill Voice" Automated="1"/>')
	voice_manager.append(f'</Parameters>')
	voice_manager.append(f'</Node>')
	return voice_manager

def add_pma(name, value, multiply, add, scaled=False, value_max=100.0, multiply_max=100.0, add_max=100.0):
	pma = []
	if scaled:
		pma.append(f'<Node ID="{name}" FactoryPath="control.pma" Bypassed="0">')
	else:
		pma.append(f'<Node ID="{name}" FactoryPath="control.pma_unscaled" Bypassed="0">')
	pma.append(f'<ModulationTargets>')
	pma.append(f'</ModulationTargets>')
	pma.append(f'<Parameters>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="{value_max}" ID="Value" Value="{value}" StepSize="0.01"/>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="{multiply_max}" ID="Multiply" Value="{multiply}"/>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="{add_max}" ID="Add" Value="{add}"/>')
	pma.append(f'</Parameters>')
	pma.append(f'</Node>')
	return pma

def add_pitch_mod(name, index=-1):
	mod = []
	mod.append(f'<Node ID="pitch_mod" FactoryPath="core.pitch_mod" Bypassed="0">')
	mod.append(f'<ModulationTargets>')
	mod.append(f'<Connection NodeId="clone_cable" ParameterId="Value"/>')
	mod.append(f'</ModulationTargets>')
	mod.append(f'<ComplexData>')
	mod.append(f'<DisplayBuffers>')
	mod.append(f'<DisplayBuffer Index="{index}"/>')
	mod.append(f'</DisplayBuffers>')
	mod.append(f'</ComplexData>')
	mod.append(f'<Parameters/>')
	mod.append(f'</Node>')
	return mod

def add_bang(name, default_value):
	bang = []
	bang.append(f'<Node ID="{name}" FactoryPath="control.voice_bang" Bypassed="0">')
	bang.append(f'<ModulationTargets>')	
	bang.append(f'</ModulationTargets>')
	bang.append(f'<Parameters>')
	bang.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="{default_value}"/>')
	bang.append(f'</Parameters>')
	bang.append(f'</Node>')
	return bang

def add_jpanner(name, default_value):
	jpanner = []
	jpanner.append(f'<Node ID="{name}" FactoryPath="jdsp.jpanner" Bypassed="0">')
	jpanner.append(f'<Parameters>')
	jpanner.append(f'<Parameter MinValue="-1.0" MaxValue="1.0" ID="Pan" Value="{default_value}"/>')
	jpanner.append(f'<Parameter MinValue="0.0" MaxValue="6.0" StepSize="1.0" ID="Rule" Value="1.0"/>')
	jpanner.append(f'</Parameters>')
	jpanner.append(f'</Node>')
	return jpanner

# this one is gross
def add_switcher(name):
	switcher = []
	switcher.append(f'<!-- Start Switcher -->')
	switcher.append(f'<Node ID="{name}" FactoryPath="container.chain" ShowParameters="1" Bypassed="0">')
	switcher.append(f'<Nodes>')
	switcher.append(f'<Node ID="switcher" FactoryPath="control.xfader" Bypassed="0">') # Start Switcher
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="NumParameters" Value="2"/>')
	switcher.append(f'<Property ID="Mode" Value="Switch"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<SwitchTargets>')
	switcher.append(f'<SwitchTarget>')
	switcher.append(f'<Connections>')
	switcher.append(f'<Connection NodeId="tanhBypass" ParameterId="Bypassed"/>') # 'tanhBypass'
	switcher.append(f'</Connections>')
	switcher.append(f'</SwitchTarget>')
	switcher.append(f'<SwitchTarget>')
	switcher.append(f'<Connections>')
	switcher.append(f'<Connection NodeId="absBypass" ParameterId="Bypassed"/>') # 'absBypass'
	switcher.append(f'</Connections>')
	switcher.append(f'</SwitchTarget>')
	switcher.append(f'</SwitchTargets>')
	switcher.append(f'<Parameters>')
	switcher.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="0.0"/>')
	switcher.append(f'</Parameters>')
	switcher.append(f'</Node>')
	switcher.append(f'<Node ID="sb_container" FactoryPath="container.chain" Bypassed="0">')
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="IsVertical" Value="0"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<Nodes>')
	switcher.append(f'<Node ID="tanhBypass" FactoryPath="container.soft_bypass" Bypassed="0">')
	switcher.append(f'<Nodes>')
	switcher.append(f'<Node ID="tanh" FactoryPath="math.expr" Bypassed="0">')
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="Code" Value="input + Math.tanh(input)"/>') # TANH
	switcher.append(f'<Property ID="Debug" Value="0"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<Parameters>')
	switcher.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	switcher.append(f'</Parameters>')
	switcher.append(f'</Node>')
	switcher.append(f'</Nodes>')
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="SmoothingTime" Value="20"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<Parameters/>')
	switcher.append(f'</Node>')
	switcher.append(f'<Node ID="absBypass" FactoryPath="container.soft_bypass" Bypassed="0">')
	switcher.append(f'<Nodes>')
	switcher.append(f'<Node ID="abs" FactoryPath="math.expr" Bypassed="0">')
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="Code" Value="input + Math.abs(input)"/>') # ABS
	switcher.append(f'<Property ID="Debug" Value="0"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<Parameters>')
	switcher.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	switcher.append(f'</Parameters>')
	switcher.append(f'</Node>')
	switcher.append(f'</Nodes>')
	switcher.append(f'<Properties>')
	switcher.append(f'<Property ID="SmoothingTime" Value="20"/>')
	switcher.append(f'</Properties>')
	switcher.append(f'<Parameters/>')
	switcher.append(f'</Node>') # End of sb2
	switcher.append(f'</Nodes>')
	switcher.append(f'<Parameters/>')
	switcher.append(f'</Node>') 
	switcher.append(f'</Nodes>') # End of sb_container
	switcher.append(f'<Parameters>')
	switcher.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Type" Value="0.0">') # CONNECT
	switcher.append(f'<Connections>')
	switcher.append(f'<Connection NodeId="switcher" ParameterId="Value"/>')
	switcher.append(f'</Connections>')
	switcher.append(f'</Parameter>')
	switcher.append(f'</Parameters>')
	switcher.append(f'</Node>')
	switcher.append(f'<!-- End Switcher -->')
	return switcher

#------------------------------------------------------------------------------------
# CONNECTIONS
#------------------------------------------------------------------------------------

def connect_module(module, connection, node_id, parameter_id):
	for idx, line in enumerate(module):
		if connection in line:
			module.insert(idx+1, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')

def create_parameter(params, name, min_value, max_value, step_size, value):
	for idx, line in enumerate(params):
		if '<Parameters>' in line:
			params.insert(idx+1, f'<Parameter ID="{name}" MinValue="{min_value}" MaxValue="{max_value}" StepSize="{step_size}" Value="{value}">')
			params.insert(idx+2, f'<Connections>')
			params.insert(idx+3, f'</Connections>')			
			params.insert(idx+4, f'</Parameter>')

def connect_parameter(params, name, node_id, parameter_id, check_for_node=False):
	for i, line in enumerate(params):
		if isinstance(line, str) and f'<Parameter ID="{name}"' in line:
			params.insert(i+2, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')
		if isinstance(line, list):
			for j, nested in enumerate(line):
				if check_for_node:
					if f'<Node ID="{name}"' in nested:
						line.insert(j+2, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')
				else:
					if f'<Parameter ID="{name}"' in nested:
						line.insert(j+2, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')




#------------------------------------------------------------------------------------
# UTILITY
#------------------------------------------------------------------------------------

def get_node_by_name(data, name):
	for idx, line in enumerate(data):
		if name in line:
			return idx