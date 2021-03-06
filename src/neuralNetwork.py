__author__ = 'windmgc'
# coding: UTF-8

from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

n = FeedForwardNetwork()
inLayer = LinearLayer(2)
hiddenLayer = SigmoidLayer(3)
outLayer = LinearLayer(1)

n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)

n.sortModules()
print n

print n.activate([1, 2])

print in_to_hidden.params
print hidden_to_out.params

means = [(-1, 0), (2, 4), (3, 1)]
cov = [diag([1, 1]), diag([0.5, 1.2]), diag([1.5, 0.7])]
alldata = ClassificationDataSet(2,1,nb_classes=3)
for n in xrange(400):
    for klass in range(3):
        input = multivariate_normal(means[klass],cov[klass])
        alldata.addSample(input,[klass])

tstdata, trndata = alldata.splitWithProportion(0.25)

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

print "Number of training patterns:", len(trndata)
print "Input and output dimensions:", trndata.indim, trndata.outdim
print "First sample(input,target,class):"
print trndata['input'][0],trndata['target'][0],trndata['class'][0]

fnn=buildNetwork(trndata.indim,5,trndata.outdim,outclass=SoftmaxLayer)
trainer = BackpropTrainer(fnn,dataset=trndata,momentum=0.1,verbose=True,weightdecay=0.01)
ticks = arange(-3.,6.,0.2)
X,Y = meshgrid(ticks,ticks)

griddata= ClassificationDataSet(2,1,nb_classes=3)
for i in xrange(X.size):
    griddata.addSample([X.ravel()[i],Y.ravel()[i]],[0])
griddata._convertToOneOfMany()

for i in range(20):
    trainer.trainEpochs(1)
    trnresult = percentError(trainer.testOnClassData(),trndata['class'])
    tstresult = percentError(trainer.testOnClassData(dataset=tstdata),tstdata['class'])
    print "epoch: %4d" % trainer.totalepochs, "train error: %5.2f%%"%trnresult, "test error: %5.2f%%" % tstresult

    out = fnn.activateOnDataset(griddata)
    out = out.argmax(axis=1)
    out = out.reshape(X.shape)

    figure(1)
    ioff()
    clf()
    hold(True)
    for c in [0,1,2]:
        here, _ = where(tstdata['class']==c)
        plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
    if out.max()!=out.min():
        contourf(X,Y,out)
    ion()
    draw()
ioff()
show()