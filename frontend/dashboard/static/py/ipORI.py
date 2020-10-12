import iptc

mAction = "Remove" ## Add xor Remove
mChain = "OUTPUT"
mTable = "FILTER"
mPolicy = ""
mProt = "udp" ## Have fixed format, if it be "" it can not use in match
mIPV = "IPV4" ## IPV4 XOR IPV6
mSourIP = "192.168.20.1"
mDestIP = "192.168.1.30"
mSourPort = "99"
mDestPort = "85"
mTarget = "ACCEPT" ## Have fixed format
mPacket = "4" ## Have NOT fixed format
mState = "" ## Have fixed format, but I don not know
mInInterface = "eth65" ## Have NOT fixed format
mOutInterface = "ABC" ## Have NOT fixed format
mMAC = ""

mWeight = ""
mName = ""
mDescription = ""


print ("Setting Table and Chain")
if mAction == "Add" :
	Adding(mChain, mTable, mPolicy, mProt, mIPV, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mPacket, mState, mInInterface, mOutInterface, mMAC)
elif mAction == "Remove" :
	Remove(mChain, mTable, mPolicy, mProt, mIPV, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mPacket, mState, mInInterface, mOutInterface, mMAC)


def Adding(mChain, mTable, mPolicy, mProt, mIPV, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mPacket, mState, mInInterface, mOutInterface, mMAC) :
	table = iptc.Table(iptc.Table.FILTER)
	if mIPV == "IPV4" :
		if mTable == "NAT" :
			table = iptc.Table(iptc.Table.NAT)
		elif mTable == "MANGLE" :
			table = iptc.Table(iptc.Table.MANGLE)
		elif mTable == "RAW" :
			table = iptc.Table(iptc.Table.RAW)
	elif mIPV == "IPV6" :
		table = iptc.Table6(iptc.Table6.FILTER)
		if mTable == "MANGLE" :
			table = iptc.Table6(iptc.Table6.MANGLE)
		elif mTable == "RAW" :
			table = iptc.Table6(iptc.Table6.RAW)
		elif mTable == "SECURITY" :
			table = iptc.Table6(iptc.Table6.SECURITY)
	
	
	policy = "DROP"
	if mPolicy == "ACCEPT" or mPolicy == "QUEUE" or mPolicy == "RETURN" :
		policy = mPolicy
	
	chain = iptc.Chain(table, mChain)
	if not table.is_chain(chain) :
		chain = iptc.Chain(table, "INPUT")
	
	rule = iptc.Rule()
	if mProt != "" :
		rule.protocol = mProt
	
	if mTarget == "ACCEPT" or mTarget == "DROP" or mTarget == "REJECT" :
		rule.target = iptc.Target(rule, mTarget)
	
	##match = rule.create_match("mark")
	if mDestPort != "" and mProt != "" :
		matchPort = iptc.Match(rule, mProt)
		matchPort.dport = mDestPort
	##	match.dport = mDestPort
		rule.add_match(matchPort)
	
	if mPacket != "" :
		matchMark = iptc.Match(rule, "mark")
		matchMark.mark = mPacket
	##	match.mark = mPacket
		rule.add_match(matchMark)
	
	if mState != "" :
		matchState = iptc.Match(rule, "state")
		matchState.state = mState
	##	match.state = mState
		rule.add_match(matchState)
	##rule.add_match(match)
	
	rule.dst = mDestIP
	rule.src = mSourIP
	
	if mInInterface != "" :
		rule.in_interface = mInInterface
	if mOutInterface != "" :
		rule.out_interface = mOutInterface
	
	chain.insert_rule(rule)
	
	print ("Checking rule setting")
	rule_exist = False
	for rule in chain.rules :
		if rule.target.name != mTarget :
			continue
		for match in rule.matches :
			if match.name != mProt :
				continue
			if match.dport != mDestPort :
				continue
			rule_exist = True
			break
		break
	
	if rule_exist :
		print ("set")
	else :
		print ("failed")

def Remove(mChain, mTable, mPolicy, mProt, mIPV, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mPacket, mState, mInInterface, mOutInterface, mMAC) :
	if mTable != "" :
		table = iptc.Table(iptc.Table.)
	
	chain = iptc.Chain(table, mChain)

	table.autocommit = False

	for rule in chain.rules :
		if () and () and (rule.in_interface and mInInterface in rule.in_interface) and (rule.out_interface and mOutInterface in rule.out_interface) :
			chain.delete_rule(rule)
	table.commit()
	table.autocommit = True
