import numpy

from variables import sample_rate
from VolumeEnvelope import VolumeEnvelope

defaultvol = 0.5

# volume envelopes are lists of times and what volume it should be at that time
volumeenvelopes = {"bell" : VolumeEnvelope([[0, 0.05], [200, 1], [800, 0.3]], 200, 0.05),
                   "flat" : VolumeEnvelope([[0, defaultvol], [400, defaultvol]], 1000, 0.1),

                   # for drums
                   "sharp" : VolumeEnvelope([[0, 1], [150, 0.2]], 100, 0),
                   "chirp" : VolumeEnvelope([[0, 1], [100, 1]], 100, 0),
                   "whisp" : VolumeEnvelope([[0, 0], [40, 1], [170, 0.2]], 100, 0)}

# volbuffers are a pair containing the volume buffer of the beginning of the volume envelope and the volume buffer for the looped section
# each buffer is a 2d numpy array with float16
volbuffers = {}

for k in volumeenvelopes:
    envelope = volumeenvelopes[k]
    n_samples = int(round(envelope.timevollist[-1][0]*sample_rate/1000))

    # then put about a second worth of the oscilation part on to the end
    n_samples2 = int(round(envelope.endoscilationrate/1000*sample_rate))
    n_samples2 = n_samples2 * (int(sample_rate/n_samples2)+1)
    firstbuf = numpy.empty((n_samples+n_samples2, 2), dtype=numpy.float)
    
    for s in range(n_samples+n_samples2):
        t = float(s)/sample_rate
        firstbuf[s][0] = envelope.tone_volume(t*1000)
        firstbuf[s][1] = firstbuf[s][0]
        
    volbuffers[k] = firstbuf

