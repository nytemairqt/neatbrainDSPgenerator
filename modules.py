#------------------------------------------------------------------------------------
# NODES
#------------------------------------------------------------------------------------

def open_chain(name, chain_type, folded=0):
	chain = []
	chain.append(f'<!-- Begin Chain {name} -->')
	chain.append(f'<Node ID="{name}" FactoryPath="{chain_type}" Bypassed="0" Folded="{folded}">') # container.chain, container.split
	chain.append(f'<Nodes>')
	return chain

def close_chain(name):
	chain = []
	chain.append(f'</Nodes>')
	chain.append(f'<Parameters/>')
	chain.append(f'</Node>')
	chain.append(f'<!-- End Chain {name} -->')
	return chain

def add_sine(name, freq_ratio):
	# maybe test adjusting the min/max limits for inter-modal randomness?
	# alternatively just use noteOn and set the ratios as parameters...
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

def add_AHDSR(name, attack, attack_level, decay, sustain, release):
	ahdsr = []
	ahdsr.append(f'<!-- AHDSR {name} -->')
	ahdsr.append(f'<Node ID="{name}" FactoryPath="envelope.ahdsr" Bypassed="0">')
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
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="10000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Attack" Value="{attack}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="AttackLevel" Value="{attack_level}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="10000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Hold" Value="20.0"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="40000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Decay" Value="{decay}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Sustain" Value="{sustain}"/>')
	ahdsr.append(f'<Parameter MinValue="0.0" MaxValue="30000.0" StepSize="0.1000000014901161" SkewFactor="0.1976716816425323" ID="Release" Value="{release}"/>')
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

def add_expr(name, code):
	expr = []
	expr.append(f'<Node ID="{name}" FactoryPath="math.expr" Bypassed="0">')
	expr.append(f'<Properties>')
	expr.append(f'<Property ID="Code" Value="{code}"/>')
	expr.append(f'<Property ID="Debug" Value="0"/>')
	expr.append(f'</Properties>')
	expr.append(f'<Parameters>')
	expr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	expr.append(f'</Parameters>')
	expr.append(f'</Node>')
	return expr

def add_tanh(name):
	tanh = []
	tanh.append(f'<Node ID="{name}" FactoryPath="math.tanh" Bypassed="0">')
	tanh.append(f'<Parameters>')
	tanh.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	tanh.append(f'</Parameters>')
	tanh.append(f'</Node>')
	return tanh

def add_abs(name):
	absolute = []
	absolute.append(f'<Node ID="{name}" FactoryPath="math.abs" Bypassed="0">')
	absolute.append(f'<Parameters>')
	absolute.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	absolute.append(f'</Parameters>')
	absolute.append(f'</Node>')
	return absolute


def add_voice_manager(name):
	voice_manager = []
	voice_manager.append(f'<Node ID="{name}" FactoryPath="envelope.voice_manager" Bypassed="0">')
	voice_manager.append(f'<Parameters>')
	voice_manager.append(f'<Parameter MinValue="0.0" MaxValue="1.0" StepSize="1.0" ID="Kill Voice" Automated="1"/>')
	voice_manager.append(f'</Parameters>')
	voice_manager.append(f'</Node>')
	return voice_manager

def add_pma(name, value, multiply, add):
	pma = []
	pma.append(f'<Node ID="{name}" FactoryPath="control.pma_unscaled" Bypassed="0">')
	pma.append(f'<ModulationTargets>')
	pma.append(f'</ModulationTargets>')
	pma.append(f'<Parameters>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="64.0" ID="Value" Value="{value}" StepSize="0.01"/>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Multiply" Value="{multiply}"/>')
	pma.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Add" Value="{add}"/>')
	pma.append(f'</Parameters>')
	pma.append(f'</Node>')
	return pma

def add_cable_expr(name, code):
	expr = []
	expr.append(f'<Node ID="{name}" FactoryPath="control.cable_expr" Bypassed="0">')
	expr.append(f'<Properties>')
	expr.append(f'<Property ID="Code" Value="{code}"/>')
	expr.append(f'<Property ID="Debug" Value="0"/>')
	expr.append(f'</Properties>')
	expr.append(f'<ModulationTargets>')
	expr.append(f'</ModulationTargets>')
	expr.append(f'<Parameters>')
	expr.append(f'<Parameter MinValue="0.0" MaxValue="1.0" ID="Value" Value="1.0"/>')
	expr.append(f'</Parameters>')
	expr.append(f'</Node>')
	return expr

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

def connect_parameter(params, name, node_id, parameter_id):
	for idx, line in enumerate(params):
		if f'<Parameter ID="{name}"' in line:
			params.insert(idx+2, f'<Connection NodeId="{node_id}" ParameterId="{parameter_id}"/>')


#------------------------------------------------------------------------------------
# UTILITY
#------------------------------------------------------------------------------------

def get_node_by_name(data, name):
	for idx, line in enumerate(data):
		if name in line:
			return idx