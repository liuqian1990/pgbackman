#!/usr/bin/env python
#
# Copyright (c) 2014 Rafael Martinez Guerrero (PostgreSQL-es)
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# This file is part of PgBackMan
# https://github.com/rafaelma/pgbackman
#
# PgBackMan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PgBackMan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PgBackMan.  If not, see <http://www.gnu.org/licenses/>.
#

import cmd
import sys
import os
import time
import signal

sys.path.append('/home/rafael/Devel/GIT/pgbackman')
from pgbackman.database import * 

# ############################################
# class pgbackman_cli
#
# This class implements the pgbackman shell.
# It is based on the python module cmd
# ############################################

class pgbackman_cli(cmd.Cmd):
    
    # ###############################
    # Constructor
    # ###############################

    def __init__(self):
        cmd.Cmd.__init__(self)
        
        self.intro =  '\n########################################################\n' + \
            'Welcome to the PostgreSQL Backup Manager shell (v.1.0.0)\n' + \
            '########################################################\n' + \
            'Type help or \? to list commands.\n'
        
        self.prompt = '[pgbackman]$ '
        self.file = None

        self.dsn = "dbname='pgbackman' user='rafael'"


    # ############################################
    # Method do_show_backup_servers
    #
    # It Implements the command show_backup_servers
    # This command  shows a list of all backup servers 
    # registered in PgBackMan
    # ############################################

    def do_show_backup_servers(self,arg):
        """
        This command  shows a list of all backup servers 
        registered in PgBackMan.

        show_backup_servers

        """
        
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            db = pgbackman_db(self.dsn)
            db.show_backup_servers()
            db.pg_close()
        else:
            print "\n* ERROR - This command does not accept parameters.\n* Type help or ? to list commands\n"
            

    # ############################################
    # Method do_register_backup_server
    #
    # It implements the command register_backup_server.
    # This command can be used to register or update 
    # a backup server in PgBackMan.
    # ############################################

    def do_register_backup_server(self,arg):
        """
        This command can be used to register or update 
        a backup server in PgBackMan.

        register_backup_server [hostname] [domain] [status] [remarks]

        RUNNING: Backup server running and online
        DOWN: Backup server not online.

        """

        db = pgbackman_db(self.dsn)
        arg_list = arg.split()

        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = "n"
            domain_default = db.get_default_backup_server_parameter("domain")
            status_default = db.get_default_backup_server_parameter("backup_server_status")

            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            ack = raw_input("# Are all values correct (y/n): ")
            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default

            if status == "":
                status = status_default
            
            if ack.lower() == "y":
                if db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status.upper().strip(),remarks.strip()):
                    print "\n* Done\n"
    
        #
        # Command with the 4 parameters that can be defined.
        # Hostname, domain, status and remarks
        #

        elif len(arg_list) >= 4:

            hostname = arg_list[0]
            domain = arg_list[1]
            status = arg_list[2]
            remarks = ""

            for i in range(3,len(arg_list)):
                remarks = remarks + " " + arg_list[i]

            if db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status.upper().strip(),remarks.strip()):
                print "\n* Done\n"

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_delete_backup_server
    #
    # It implements the command delete_backup_server.
    # This command can be used to delete a backup 
    # server registered in PgBackMan.
    # ############################################

    def do_delete_backup_server(self,arg):
        """
        This command can be used to delete a backup 
        server registered in PgBackMan.

        delete_backup_server [SrvID | FQDN]

        """
        
        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN: ")
            print
            ack = raw_input("# Are you sure you want to delete this server? (y/n): ")
            print "--------------------------------------------------------"

            if ack.lower() == "y":
                if server_id.isdigit():
                    if db.delete_backup_server(db.get_backup_server_fqdn(server_id)):
                        print "\n* Done\n"
                else:
                    if db.delete_backup_server(server_id):
                        print "\n* Done\n"
                    
        elif len(arg_list) == 1:

            server_id = arg_list[0]
            
            if server_id.isdigit():
                if db.delete_backup_server(db.get_backup_server_fqdn(server_id)):
                    print "\n* Done\n"
            else:
                if db.delete_backup_server(server_id):
                    print "\n* Done\n"
                    
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()

        


    # ############################################
    # Method do_show_pgsql_nodes
    #
    # It Implements the command show_pgsql_nodes
    # This command  shows a list of all postgreSQL 
    # nodes registered in PgBackMan
    # ############################################

    def do_show_pgsql_nodes(self,arg):
        """
        This command  shows a list of all postgreSQL
        nodes registered in PgBackMan.
        
        show_pgsql_nodes
              
        """
        
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            db = pgbackman_db(self.dsn)
            db.show_pgsql_nodes()
            db.pg_close()
        else:
            print "\n* ERROR - This command does not accept parameters.\n* Type help or ? to list commands\n"
            
            
            
    # ############################################
    # Method do_register_pgsql_node
    #
    # It implements the command register_pgsql_node.
    # This command can be used to register or update 
    # a postgreSQL node in PgBackMan.
    # ############################################
            
    def do_register_pgsql_node(self,arg):
        """
        This command can be used to register or update 
        a postgreSQL node in PgBackMan.

        register_pgsql_node [hostname] [domain] [pgport] [admin_user] [status] [remarks]

        Status:
        -------
        RUNNING: PostgreSQL node running and online
        DOWN: PostgreSQL node not online.

        """
        
        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = "n"
            domain_default = db.get_default_pgsql_node_parameter("domain")
            port_default = db.get_default_pgsql_node_parameter("pgport")
            admin_user_default = db.get_default_pgsql_node_parameter("admin_user")
            status_default = db.get_default_pgsql_node_parameter("pgsql_node_status")
            
            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            port = raw_input("# Port [" + port_default + "]: ")
            admin_user = raw_input("# Admin user [" + admin_user_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            ack = raw_input("# Are all values correct (y/n): ")
            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default

            if port == "":
                port = port_default

            if admin_user == "":
                admin_user = admin_user_default
                
            if status == "":
                status = status_default
            
            if ack.lower() == "y":
                if self.check_digit(port):
                    if db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip()):
                        print "\n* Done\n"
        
        #
        # Command with the 6 parameters that can be defined.
        # Hostname, domain, pgport, admin_user, status and remarks
        #

        elif len(arg_list) >= 6:

            hostname = arg_list[0]
            domain = arg_list[1]
            port = arg_list[2]
            admin_user = arg_list[3]
            status = arg_list[4]
            remarks = ""

            for i in range(5,len(arg_list)):
                remarks = remarks + " " + arg_list[i]

            if self.check_digit(port):   
                if db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip()):
                    print "\n* Done\n"

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_delete_pgsql_node
    #
    # It implements the command delete_pgsql_node
    # This command can be used to delete a postgreSQL 
    # node defined in PgBackMan.
    # ############################################

    def do_delete_pgsql_node(self,arg):
        """
        This command can be used to delete a postgreSQL 
        node defined in PgBackMan.
        
        delete_pgsql_node [NodeID | FQDN]
        
        """

        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            node_id = raw_input("# NodeID / FQDN: ")
            print
            ack = raw_input("# This action will also DELETE ALL BACKUP JOBS definitions for this PgSQL node.\n# Are you sure you want to delete this PgSQL node? (y/n): ")
           

            if ack.lower() == "y":

                ack2= raw_input("\n# Are you 110% sure you want to do this?\n# There is no way back after this point (yes/no): ") 
                print "--------------------------------------------------------"

                if ack2.lower() == "yes":
                    if node_id.isdigit():
                        if db.delete_pgsql_node(db.get_pgsql_node_fqdn(node_id)):
                            print "\n* Done\n"
                    else:
                        if db.delete_pgsql_node(node_id):
                            print "\n* Done\n"
            else:
                print "--------------------------------------------------------"

        elif len(arg_list) == 3:

            node_id = arg_list[0]
            ack =  arg_list[1]
            ack2 =  arg_list[2]
            
            if ack.lower() == "y" and ack2.lower() == "yes":
                if node_id.isdigit():
                    if db.delete_pgsql_node(db.get_pgsql_node_fqdn(node_id)):
                        print "\n* Done\n"
                else:
                    if db.delete_pgsql_node(node_id):
                        print "\n* Done\n"
                
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()

        

    # ############################################
    # Method do_show_backup_server_job_definitions
    # ############################################

    def do_show_backup_server_job_definitions(self,arg):
        """
        show_backup_server_job_definitions [SrvID | FQDN]


        """
        
        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN: ")
            print "--------------------------------------------------------"

            if server_id.isdigit():
                if db.show_backup_server_job_definitions(db.get_backup_server_fqdn(server_id)):
                    print "\n* Done\n"
            else:
                if db.show_backup_server_job_definitions(server_id):
                        print "\n* Done\n"
                    
        elif len(arg_list) == 1:

            server_id = arg_list[0]
            
            if server_id.isdigit():
                if db.show_backup_server_job_definitions(db.get_backup_server_fqdn(server_id)):
                    print "\n* Done\n"
            else:
                if db.show_backup_server_job_definitions(server_id):
                    print "\n* Done\n"
                    
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_show_pgsql_node_job_definitions
    # ############################################

    def do_show_pgsql_node_job_definitions(self,arg):
        """
        show_pgsql_node_job_definitions [NodeID | FQDN]


        """
        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            node_id = raw_input("# NodeID / FQDN: ")
            print "--------------------------------------------------------"

            if node_id.isdigit():
                if db.show_pgsql_node_job_definitions(db.get_pgsql_node_fqdn(node_id)):
                    print "\n* Done\n"
            else:
                if db.show_pgsql_node_job_definitions(node_id):
                        print "\n* Done\n"
                    
        elif len(arg_list) == 1:

            node_id = arg_list[0]
            
            if node_id.isdigit():
                if db.show_pgsql_node_job_definitions(db.get_pgsql_node_fqdn(node_id)):
                    print "\n* Done\n"
            else:
                if db.show_pgsql_node_job_definitions(node_id):
                    print "\n* Done\n"
                    
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_show_database_job_definitions
    # ############################################

    def do_show_database_job_definitions(self,arg):
        """
        show_database_job_definitions [DBname]


        """

        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            dbname = raw_input("# DBname: ")
            print "--------------------------------------------------------"
            
            if db.show_database_job_definitions(dbname):
                print "\n* Done\n"
                
                    
        elif len(arg_list) == 1:

            dbname = arg_list[0]
            
            if db.show_database_job_definitions(dbname):
                print "\n* Done\n"
                
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_register_backup_job
    # ############################################

    def do_register_backup_job_definition(self,arg):
        """
        This command can be used to register or update 
        a backup job definition in PgBackMan.

        register_backup_job_definition [SrvID | FQDN] [NodeID | FQDN] [DBname] 
                                       [mincron] [hourcron] [weekdaycron] [monthcron] [daymonthcron] 
                                       [backup code] [encryption] 
                                       [retention period] [retention redundancy] 
                                       [extra params] [job status] [remarks] 

        Backup code: 
        ------------
        FULL: Full Backup of a database. Schema + data + owner globals + db_parameters.
        SCHEMA: Schema backup of a database. Schema + owner globals + db_parameters.
        DATA: Data backup of the database.

        Job status:
        -----------
        ACTIVE: Backup job activated and in production.
        STOPPED: Backup job stopped.

        Encryption:
        -----------
        TRUE: GnuPG encryption activated.
        FALSE: GnuPG encryption NOT activated.

        """

        db = pgbackman_db(self.dsn)
        arg_list = arg.split()
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = "n"
         
            minutes_cron_default = hours_cron_default = weekday_cron_default = month_cron_default = day_month_cron_default = \
                backup_code_default = encryption_default = retention_period_default = retention_redundancy_default = \
                extra_parameters_default = backup_job_status_default = ""

            minutes_cron_default = db.get_minute_from_interval(db.get_default_pgsql_node_parameter("backup_minutes_interval"))
            hours_cron_default = db.get_hour_from_interval(db.get_default_pgsql_node_parameter("backup_hours_interval"))
            weekday_cron_default = db.get_default_pgsql_node_parameter("backup_weekday_cron")
            month_cron_default = db.get_default_pgsql_node_parameter("backup_month_cron")
            day_month_cron_default = db.get_default_pgsql_node_parameter("backup_day_month_cron")
            backup_code_default = db.get_default_pgsql_node_parameter("backup_code")
            encryption_default = db.get_default_pgsql_node_parameter("encryption")
            retention_period_default = db.get_default_pgsql_node_parameter("retention_period")
            retention_redundancy_default = db.get_default_pgsql_node_parameter("retention_redundancy")
            extra_parameters_default = db.get_default_pgsql_node_parameter("extra_parameters")
            backup_job_status_default = db.get_default_pgsql_node_parameter("backup_job_status")

            
            print "--------------------------------------------------------"
            backup_server = raw_input("# Backup server FQDN []: ")
            pgsql_node = raw_input("# PgSQL node FQDN  []: ")
            dbname = raw_input("# DBname []: ")
            minutes_cron = raw_input("# Minutes cron [" + str(minutes_cron_default) + "]: ")
            hours_cron = raw_input("# Hours cron [" + str(hours_cron_default) + "]: ")
            weekday_cron = raw_input("# Weekday cron [" + weekday_cron_default + "]: ")
            month_cron = raw_input("# Month cron [" + month_cron_default + "]: ")
            day_month_cron = raw_input("# Day-month cron [" + day_month_cron_default + "]: ")
            backup_code = raw_input("# Backup code [" + backup_code_default + "]: ")
            encryption = raw_input("# Encryption [" + encryption_default + "]: ")
            retention_period = raw_input("# Retention period [" + retention_period_default + "]: ")
            retention_redundancy = raw_input("# Retention redundancy [" + retention_redundancy_default + "]: ")
            extra_parameters = raw_input("# Extra parameters [" + extra_parameters_default + "]: ")
            backup_job_status = raw_input("# Job status [" + backup_job_status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            ack = raw_input("# Are all values correct (y/n): ")
            print "--------------------------------------------------------"

            if minutes_cron == "":
                minutes_cron = str(minutes_cron_default)

            if hours_cron == "":
                hours_cron = str(hours_cron_default)

            if weekday_cron == "":
                weekday_cron = weekday_cron_default

            if month_cron == "":
                month_cron = month_cron_default

            if day_month_cron == "":
                day_month_cron = day_month_cron_default

            if backup_code == "":
                backup_code = backup_code_default

            if encryption == "":
                encryption = encryption_default

            if retention_period == "":
                retention_period = retention_period_default

            if retention_redundancy == "":
                retention_redundancy = retention_redundancy_default

            if extra_parameters == "":
                extra_parameters = extra_parameters_default

            if backup_job_status == "":
                backup_job_status = backup_job_status_default
            

            print ((backup_server,pgsql_node,dbname,minutes_cron,hours_cron, \
                                              weekday_cron,month_cron,day_month_cron,backup_code,encryption, \
                                              retention_period,retention_redundancy,extra_parameters,backup_job_status,remarks))

            if ack.lower() == "y":
                if db.register_backup_job(backup_server.lower().strip(),pgsql_node.lower().strip(),dbname.strip(),minutes_cron,hours_cron, \
                                              weekday_cron.strip(),month_cron.strip(),day_month_cron.strip(),backup_code.upper().strip(),encryption.lower().strip(), \
                                              retention_period.lower().strip(),retention_redundancy.strip(),extra_parameters.lower().strip(),backup_job_status.upper().strip(),remarks.strip()):
                    print "\n* Done\n"
        
        #
        # Command with the 6 parameters that can be defined.
        # Hostname, domain, pgport, admin_user, status and remarks
        #

        elif len(arg_list) >= 15:

            backup_server = arg_list[0]
            pgsql_node = arg_list[1]
            dbname = arg_list[2]
            minutes_cron = arg_list[3]
            hours_cron = arg_list[4]
            weekday_cron = arg_list[5]
            month_cron = arg_list[6]
            day_month_cron = arg_list[7]
            backup_code = arg_list[8]
            encryption = arg_list[9]
            retention_period = arg_list[10]
            retention_redundancy = arg_list[11]
            extra_parameters = arg_list[12]
            backup_job_status = arg_list[13]
            remarks = arg_list[14]

            for i in range(15,len(arg_list)):
                remarks = remarks + " " + arg_list[i]

                
            if db.register_backup_job(backup_server.lower().strip(),pgsql_node.lower().strip(),dbname.strip(),minutes_cron,hours_cron, \
                                          weekday_cron.strip(),month_cron.strip(),day_month_cron.strip(),backup_code.upper().strip(),encryption.lower().strip(), \
                                          retention_period.lower().strip(),retention_redundancy.strip(),extra_parameters.lower().strip(),backup_job_status.upper().strip(),remarks.strip()):
                print "\n* Done\n"

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()




    # ############################################
    # Method do_delete_backup_job
    # ############################################

    def do_delete_backup_job_definition(self,arg):
        """
        delete_backup_job_definition [BckID]

        """


    # ############################################
    # Method do_show_backup_server_catalog
    # ############################################

    def do_show_backup_server_catalog(self,arg):
        """
        show_backup_server_catalog [SrvID]

        """

    # ############################################
    # Method do_show_pgsql_node_catalog
    # ############################################

    def do_show_pgsql_node_catalog(self,arg):
        """
        show_pgsql_node_catalog [NodeID | FQDN]

        """

    # ############################################
    # Method do_show_database_catalog
    # ############################################

    def do_show_database_catalog(self,arg):
        """
        show_database_catalog [DBname]

        """

    # ############################################
    # Method do_show_backup_job_details
    # ############################################

    def do_show_database_catalog_details(self,arg):
        """
        show_database_catalog_details [BckID]

        """

    # ############################################
    # Method do_show_pgbackman_config
    # ############################################

    def do_show_pgbackman_config(self,arg):
        """
        show_pgbackman_config

        """

    # ############################################
    # Method do_show_pgbackman_stats
    # ############################################

    def do_show_pgbackman_stats(self,arg):
        """
        show_pgbackman_stats

        """    

    # ############################################
    # Method do_show_backup_server_stats
    # ############################################

    def do_show_backup_server_stats(self,arg):
        """
        show_backup_server_stats [SrvID]

        """    

    # ############################################
    # Method do_show_pgsql_node_stats
    # ############################################

    def do_show_pgsql_node_stats(self,arg):
        """
        show_pgsql_node_stats [NodeID]

        """    

    # ############################################
    # Method do_show_job_queue
    # ############################################

    def do_show_job_queue(self,arg):
        """
        show_pgsql_job_queue

        """   
 
    # ############################################
    # Method do_show_backup_server_default_config
    # ############################################

    def do_show_backup_server_default_config(self,arg):
        """
        show_backup_server_default_config [SrvID | FQDN]

        """    

    # ############################################
    # Method do_show_pgsql_node_default_config
    # ############################################

    def do_show_pgsql_node_default_config(self,arg):
        """
        show_pgsql_node_default_config [NodeID | FQDN]

        """    


    # ############################################
    # Method do_clear
    # ############################################

    def do_clear(self,arg):
        """Command clear"""
        
        os.system('clear')
        print self.intro


    # ############################################
    # Method default
    # ############################################

    def default(self,line):
        print "* Unknown command: %s \n* Type help or \? to list commands\n" % line


    # ############################################
    # Method emptyline
    # ############################################

    def emptyline(self):
        pass


    # ############################################
    # Method precmd
    # ############################################

    def precmd(self, line_in):
        if line_in != 'EOF':
            line_out = line_in.lower()
        else:
            line_out = line_in

        if line_out == "\h":
            line_out = "help"
        elif line_out == "\?":
            line_out = "help"
        elif line_out == "\s":
            line_out = "hist"    
        elif line_out == "\q":
            line_out = "quit" 
        elif line_out == "\!":
            line_out = "shell"
    
        self._hist += [ line_out.strip() ]
          
        return cmd.Cmd.precmd(self, line_out)


    # ############################################
    # Method do_shell
    # ############################################

    def do_shell(self, line):
        "Run a shell command"
        
        try:
            os.system(line)
        except:
            print "* Problems running '%s'" % line


    # ############################################
    # Method do_quit
    # ############################################

    def do_quit(self, arg):
        'Quit the PgBackMan shell.'
        
        print "\nDone, thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_EOF
    # ############################################
    
    def do_EOF(self, line):
        'Quit the PgBackMan shell.'
        
        print
        print "Thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_hist
    # ############################################

    def do_show_history(self, args):
        """Print a list of commands that have been entered"""

        print self._hist


    # ############################################
    # Method preloop
    # ############################################

    def preloop(self):
        """
        Initialization before prompting user for commands.
        """
        
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}


    # ############################################
    # Method help_shortcuts
    # ############################################

    def help_shortcuts(self):
        """Help information about shortcuts in PgBackMan"""
        
        print """
        Shortcuts in PgBackMan:

        \h [NAME] - Help on syntax of PgBackMan commands
        \? [COMMAND] - Help on syntax of PgBackMan commands
        
        \s - display history 
        \q - quit PgBackMan shell

        \! [COMMAND] - Execute command in shell
          
        """

    # ############################################
    # Method handler
    # ############################################

    def signal_handler(self,signum, frame):
        cmd.Cmd.onecmd(self,'quit')
        sys.exit(0)


    # ############################################
    # Method check_digit
    # ############################################

    def check_digit(self,digit):
        
        if digit.isdigit():
            return True
        else:
            print "\n* ERROR - %s should be a digit\n" % digit 
            return False



signal.signal(signal.SIGINT, pgbackman_cli().signal_handler)


if __name__ == '__main__':
    pgbackman_cli().cmdloop()
