#!/usr/local/bin/python3
from Vagrant import Vagrant
import rumps
from apscheduler.schedulers.background import BackgroundScheduler

# Callbacks
def cb_vm_destroy(sender):
    sender.vm.destroy()

def cb_vm_power_off(sender):
    sender.vm.poweroff()

def cb_vm_power_on(sender):
    sender.vm.poweron()

def cb_vm_provision(sender):
    sender.vm.provision()

def cb_vm_reset(sender):
    sender.vm.reset()

def cb_vm_ssh(sender):
    sender.vm.ssh()

def cb_vm_web(sender):
    sender.vm.web()

class VagrantBar(rumps.App):

    vagrant = None # Store our vagrant instance

    def __init__(self):
        super(VagrantBar, self).__init__(name="VB", icon="assets/icon.png")

        self.vagrant = Vagrant()

        self.menu = []
        self.build_menu()
        self.menu.add('')


        # Here we update the menu in the background:
        sched = BackgroundScheduler()

        def scheduled_updater():
            self.update_menu()

        sched.add_job(scheduled_updater, 'interval', seconds=5)
        sched.start()


    def build_menu(self):
        for name,vm in self.vagrant.get_vms():
            if name not in self.menu:
                submenu = rumps.MenuItem(name)
                    
                if vm.state == Vagrant.STATE_POWERON:
                    submenu.state = 1 
                    submenu.add(self.create_menu_item("Power Off", vm, cb_vm_power_off))
                    submenu.add(self.create_menu_item("Reset", vm, cb_vm_reset))
                    submenu.add(self.create_menu_item("Reprovision", vm, cb_vm_provision))
                    submenu.add('')
                    submenu.add(self.create_menu_item("Open SSH Console", vm, cb_vm_ssh))
                    submenu.add(self.create_menu_item("Open in Browser", vm, cb_vm_web))
                else:
                    submenu.state = 0
                    submenu.add(self.create_menu_item("Power On", vm, cb_vm_power_on))
                    submenu.add('')
                    submenu.add(self.create_menu_item("Destroy", vm, cb_vm_destroy))

                self.menu.add(submenu)


            else:
                item = self.menu[name]
                if item.state == 0 and vm.state == Vagrant.STATE_POWERON or item.state == 1 and vm.state == Vagrant.STATE_POWEROFF:
                    # Update here!
                    item.clear()
                    if vm.state == Vagrant.STATE_POWERON:
                        item.state = 1
                        item.add(self.create_menu_item("Power Off", vm, cb_vm_power_off))
                        item.add(self.create_menu_item("Reset", vm, cb_vm_reset))
                        item.add(self.create_menu_item("Reprovision", vm, cb_vm_provision))
                        item.add('')
                        item.add(self.create_menu_item("Open SSH Console", vm, cb_vm_ssh))
                        item.add(self.create_menu_item("Open in Browser", vm, cb_vm_web))
                    else:
                        item.state = 0
                        item.add(self.create_menu_item("Power On", vm, cb_vm_power_on))
                        item.add('')
                        item.add(self.create_menu_item("Destroy", vm, cb_vm_destroy))

                

    def update_menu(self):
        self.vagrant.update_vms()
        self.build_menu()

    def create_menu_item(self, title, vm, callback):
        item = rumps.MenuItem(title, callback=callback)
        item.vm = vm
        return item

if __name__ == "__main__":
    VagrantBar().run()

