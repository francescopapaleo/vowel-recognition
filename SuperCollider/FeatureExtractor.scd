
s.boot // Boot the server first

(
x = Task.new({
	~vowelA = [1620, 780]; // A
	~vowelE = [2150, 440]; // E
	~vowelI = [2300, 300]; // I
	~vowelO = [900, 580]; // O
	~vowelU = [780, 290]; // U
	"fatto".postln;
	// PREPARE OUTPUT NETWORK FRANCESCO
	~outputIP = "127.0.0.1";
	~outputPort = 6448;
	~outputNet = NetAddr.new(~outputIP, ~outputPort);
	~arrayOSC = [0.0, 0.0, 0.0, 0.0, 0.0];
	~arrayOSCounter = 0;
	~oscFunc = OSCFunc({ arg msg, time;
		var value;
		value = msg[3]; // Prende il valore del sig
		~arrayOSCounter = ~arrayOSCounter + 1 % 5;
		case
		{~arrayOSCounter==1} {~arrayOSC[0] = value}
		{~arrayOSCounter==2} {~arrayOSC[1] = value}
		{~arrayOSCounter==3} {~arrayOSC[2] = value}
		{~arrayOSCounter==4} {~arrayOSC[3] = value}
		{~arrayOSCounter==0} {~arrayOSC[4] = value; ~outputNet.sendMsg("/wek/inputs", ~arrayOSC[0], ~arrayOSC[1], ~arrayOSC[2], ~arrayOSC[3], ~arrayOSC[4]); ~arrayOSC.postln};

	},'/tr', s.addr);

	SynthDef(\vowels, {|filterReson = 0.05, f1 = 1620, f2 = 780, sourceFreq = 70, amp = 1.0|
		var aFilter, eFilter, iFilter, oFilter, uFilter,
		output, input,
		rmsA, rmsE, rmsI, rmsO, rmsU,
		chain1, chain2, magnitudeAbove, localMax, loudnessTracker, triggerInterval, detect, gate;

		//input = BPF.ar(Saw.ar(sourceFreq), f1, 1.0) + BPF.ar(Saw.ar(sourceFreq), f2, 1.0);
		//input = PinkNoise.ar(0.1);
		input = SoundIn.ar(0);


		// GATE PART
		chain1 = FFT(LocalBuf(2048), input);
		loudnessTracker = Loudness.kr(chain1); // If loudness > 20 gate aperto
		loudnessTracker = (loudnessTracker - 15); // -15 Threshold
		gate = Select.kr(loudnessTracker > DC.kr(0.0), [DC.ar(0.0), DC.ar(1.0)]);
		input = input * gate;

		// AMPLITUDE NORMALISATION AND SPECTRAL LOCAL MAX FILTERING
		input = Normalizer.ar(input); // Amplitude normalization
		input = HPF.ar(input, 100); // Don't consider vowels under 100
		input = LPF.ar(input, 3000); // Don't consider vowels over 3000
		chain2 = FFT(LocalBuf(2048), input);
		localMax = PV_LocalMax(chain2, 30); // Try 0-50.0
		input = IFFT(localMax);


		aFilter = [BBandPass.ar(input, ~vowelA[0], filterReson), BBandPass.ar(input, ~vowelA[1], filterReson)];
		aFilter = Mix.ar(aFilter);

		eFilter = [BBandPass.ar(input, ~vowelE[0], filterReson), BBandPass.ar(input, ~vowelE[1], filterReson)];
		eFilter = Mix.ar(eFilter);

		iFilter = [BBandPass.ar(input, ~vowelI[0], filterReson), BBandPass.ar(input, ~vowelI[1], filterReson)];
		iFilter = Mix.ar(iFilter);

		oFilter = [BBandPass.ar(input, ~vowelO[0], filterReson), BBandPass.ar(input, ~vowelO[1], filterReson)];
		oFilter = Mix.ar(oFilter);

		uFilter = [BBandPass.ar(input, ~vowelU[0], filterReson), BBandPass.ar(input, ~vowelU[1], filterReson)];
		uFilter = Mix.ar(uFilter);


		rmsA = RunningSum.rms(aFilter, 1200) * 1000;
		rmsE = RunningSum.rms(eFilter, 1200) * 1000;
		rmsI = RunningSum.rms(iFilter, 1200) * 1000;
		rmsO = RunningSum.rms(oFilter, 1200) * 1000;
		rmsU = RunningSum.rms(uFilter, 1200) * 1000;


		triggerInterval = s.options.blockSize; // Interval to send OSC messages
		//triggerInterval = 1; // Interval to send OSC messages

		SendTrig.ar(Impulse.ar(triggerInterval), 0, rmsA);
		SendTrig.ar(Impulse.ar(triggerInterval), 1, rmsE);
		SendTrig.ar(Impulse.ar(triggerInterval), 2, rmsI);
		SendTrig.ar(Impulse.ar(triggerInterval), 3, rmsO);
		SendTrig.ar(Impulse.ar(triggerInterval), 4, rmsU);

	}
	).play;

}).play
)