#!/usr/bin/env python

from os import system
from sys import argv
import time

class GCInstance:
	def __init__(self, name):
		self.instance = name
		self.project = "ivory-infusion-209508" 
		self.zone = "europe-west1-b" 

	def local(self, cmd):
		print(cmd)
		system(cmd)

	def createCustom(self, cores=1, ram=1024):
		self.create(f"custom-{cores}-{ram}")

	#n1-highcpu-8
	def create(self, machine="f1-micro", args = "--preemptible"):
		self.delete()
		self.local(
			f'gcloud beta compute --project=ivory-infusion-209508 instances create {self.instance} --zone=europe-west1-b --machine-type={machine} --subnet=default --network-tier=PREMIUM --no-restart-on-failure --maintenance-policy=TERMINATE {args} --service-account=470010940365-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --disk=name=miaou,device-name=miaou,mode=rw,boot=yes'
		)


	def stopScript(self, script):
		self.local(
			f'gcloud compute --project {self.project}  instances add-metadata {self.instance} --metadata-from-file shutdown-script={script} --zone "{self.zone}"'
		)

	def start(self):
		self.local(
			f'gcloud compute --project "{self.project}" instances start --zone "{self.zone}" "{self.instance}"'
		)
		time.sleep(60) 


	def stopHours(self, hours):
		self.remote(f'sudo shutdown -P +{int(hours * 60)}')

	def stop(self):
		self.remote('sudo shutdown -P now')

	def delete(self):
		self.local(
			f'gcloud compute --project "{self.project}" instances delete "{self.instance}"  --zone "{self.zone}" --keep-disks all --quiet'
		)

	def remote(self, cmd):
		self.local(
			f'gcloud compute --project "{self.project}" ssh --zone "{self.zone}" "{self.instance}" -- "{cmd}"'
		)

	def localToRemote(self, source, target):
		self.remote(f"rm -rf {target}")
		self.local(
			f'gcloud compute --project "{self.project}" scp --zone "{self.zone}" {source} {self.instance}:{target}'
		)

	def remoteToLocal(self, source, target):
		self.remote(f"rm -rf {target}")
		self.local(
			f'gcloud compute --project "{self.project}" scp --zone "{self.zone}" {self.instance}:{source} {target}'
		)

#setsid nohup (sbt test;sudo poweroff) &> sbtTest.txt
