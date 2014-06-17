# Python Libraries
from __future__ import print_function
from __future__ import division
import sys
import os.path
lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(lib_path)
import argparse
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy
import time, datetime, getpass, fnmatch, HTML

# Local Libraries
# Distal Libraries
from rgt.GenomicRegionSet import *
from rgt.ExperimentalMatrix import *
from rgt.Util import GenomeData
from plotTools import *

dir = os.getcwd()
"""
Statistical analysis methods and plotting tools for ExperimentalMatrix

Author: Joseph Kuo

"""

#################################################################################################
##### FUNCTIONS #################################################################################
#################################################################################################
    

######### Universal functions
def print2(parameter, string):
    """ Show the message on the console and also save in a list for future backup. """
    print(string)
    parameter.append(string)
    
######### Projection test

def output(f, directory, folder, filename, extra=None):
    """Output the file in the defined folder """
    pd = os.path.join(dir,directory,folder)
    try:
        os.stat(os.path.dirname(pd))
    except:
        os.mkdir(os.path.dirname(pd))
    try:
        os.stat(pd)
    except:
        os.mkdir(pd)    
    
    # Saving 
    if extra == None:
        f.savefig(os.path.join(pd,filename), bbox_inches='tight',dpi=300)
    else:
        f.savefig(os.path.join(pd,filename), bbox_extra_artists=(extra), bbox_inches='tight',dpi=300)
    
    if args.pdf:
        pp = PdfPages(os.path.join(pd,filename) + '.pdf')
        pp.savefig(f, bbox_extra_artists=(extra),bbox_inches='tight') 
    
        # Set the file's metadata via the PdfPages object:
        d = pp.infodict()
        d['Title'] = args.title
        d['CreationDate'] = datetime.datetime.today()
        pp.close()
    
    if args.show:
        plt.show()
        
def output_parameters(parameter, directory, folder, filename):
    pd = os.path.join(dir,directory,folder)
    try:
        os.stat(os.path.dirname(pd))
    except:
        os.mkdir(os.path.dirname(pd))
    try:
        os.stat(pd)
    except:
        os.mkdir(pd)    
    if parameter:
        logp = open(os.path.join(pd,"parameters.txt"),'w')
        for s in parameter:
            logp.write("{}\n".format(s))
        logp.close()



######### 
#########
######### 
######### 
#########     
    

#################################################################################################
##### PARAMETERS ################################################################################
#################################################################################################

# Some general help descriptions
######### Some general plotting arguments descriptions ###############
helpinput = 'The file name of the input Experimental Matrix file. Recommended to add more columns for more information for ploting. For example, cell type or factors.'
helpoutput = 'The directory name for the output files. For example, project name.'
helptitle = 'The title shown on the top of the plot and also the folder name.'
helpgroup = "Group the data by reads(needs 'factor' column), regions(needs 'factor' column), another name of column (for example, 'cell')in the header of experimental matrix, or None."
helpsort = "Sort the data by reads(needs 'factor' column), regions(needs 'factor' column), another name of column (for example, 'cell')in the header of experimental matrix, or None."
helpcolor = "Color the data by reads(needs 'factor' column), regions(needs 'factor' column), another name of column (for example, 'cell')in the header of experimental matrix, or None."
helpDefinedColot = 'Define the specific colors with the given column "color" in experimental matrix. The color should be in the format of matplotlib.colors. For example, "r" for red, "b" for blue, or "(100, 35, 138)" for RGB.'
helpreference = 'The file name of the reference Experimental Matrix. Multiple references are acceptable.'
helpquery = 'The file name of the query Experimental Matrix. Multiple queries are acceptable.'

parser = argparse.ArgumentParser(description='Provides various Statistical analysis methods and plotting tools for ExperimentalMatrix.\
\nAuthor: Joseph Kuo, Ivan Gesteira Costa Filho', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(help='sub-command help',dest='mode')

################### Projection test ##########################################
parser_projection = subparsers.add_parser('projection',help='Projection test evaluates the association level by comparing to the random binomial model. \
The null hypothesis is that no association between reference and query and their distribution is random.')
parser_projection.add_argument('output', help=helpoutput) 
parser_projection.add_argument('-r', '--reference',help=helpreference)
parser_projection.add_argument('-q', '--query', help=helpquery)
parser_projection.add_argument('-t','--title', default='projection_test', help=helptitle)
parser_projection.add_argument('-g', default=None, help=helpgroup +" (Default:None)")
parser_projection.add_argument('-c', default="regions", help=helpcolor +' (Default: regions)')
parser_projection.add_argument('-intersect', action="store_true", help='Take the intersect of references as background for binominal test.')
parser_projection.add_argument('-organism',default='hg19', help='Define the organism. (Default: hg19)')
parser_projection.add_argument('-log', action="store_true", help='Set y axis of the plot in log scale.')
parser_projection.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_projection.add_argument('-pdf', action="store_true", help='Save the plot in pdf format.')
parser_projection.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_projection.add_argument('-show', action="store_true", help='Show the figure in the screen.')
parser_projection.add_argument('-table', action="store_true", help='Store the tables of the figure in text format.')

################### Jaccard test ##########################################

parser_jaccard = subparsers.add_parser('jaccard',help='Jaccard test evaluate the association level by comparing with jaccard index from repeating randomization.')

parser_jaccard.add_argument('output', help=helpoutput) 
parser_jaccard.add_argument('-r', '--reference',help=helpreference)
parser_jaccard.add_argument('-q', '--query', help=helpquery)
parser_jaccard.add_argument('-t','--title', default='jaccard_test', help=helptitle)
parser_jaccard.add_argument('-rt','--runtime', type=int, default=500, help='Define how many times to run the randomization.')
parser_jaccard.add_argument('-g', default=None, help=helpgroup +" (Default:None)")
parser_jaccard.add_argument('-c', default="regions", help=helpcolor +' (Default: regions)')
parser_jaccard.add_argument('-organism',default='hg19', help='Define the organism. (Default: hg19)')
parser_jaccard.add_argument('-log', action="store_true", help='Set y axis of the plot in log scale.')
parser_jaccard.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_jaccard.add_argument('-pdf', action="store_true", help='Save the plot in pdf format.')
parser_jaccard.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_jaccard.add_argument('-show', action="store_true", help='Show the figure in the screen.')

################### Intersect Test ##########################################
parser_intersect = subparsers.add_parser('intersection',help='Intersection test provides various modes of intersection to test the association between references and queries.')

parser_intersect.add_argument('output', help=helpoutput)
parser_intersect.add_argument('-r', '--reference',help=helpreference)
parser_intersect.add_argument('-q', '--query', help=helpquery)
parser_intersect.add_argument('-t','--title', default='intersection_test', help=helptitle)
parser_intersect.add_argument('-g', type=str, help=helpgroup +" (Default:None)")
parser_intersect.add_argument('-c', default="regions", help=helpcolor +' (Default: regions)')
parser_intersect.add_argument('-organism',default='hg19', help='Define the organism. (Default: hg19)')
parser_intersect.add_argument('-m', default="OVERLAP", choices=['OVERLAP','ORIGINAL','COMP_INCL'], 
                              help="Define the mode for intersection. \
                              'OVERLAP' defines the true intersections which are included in both reference and query, \
                              'ORIGINAL' defines the intersection as the regions of reference which have any intersections with query,\
                              'COMP_INCL' defines the intersection as the regions of query which are completely included by reference.")
parser_intersect.add_argument('-stackedbar', action="store_true", help='Plot the intersection test in stacked bar plot according to their intersections.')
parser_intersect.add_argument('-pbar', action="store_true", help='Plot the intersection test in stacked bar with percentage.')
parser_intersect.add_argument('-log', action="store_true", help='Set y axis of the plot in log scale.')
parser_intersect.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_intersect.add_argument('-pdf', action="store_true", help='Save the plot in pdf format.')
parser_intersect.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_intersect.add_argument('-show', action="store_true", help='Show the figure in the screen.')

################### Combinatorial code ##########################################
parser_combinatorial = subparsers.add_parser('combinatorial',help='Combinatorial code analyzes various associations between references and queries.')

parser_combinatorial.add_argument('output', help=helpoutput)
parser_combinatorial.add_argument('-r', '--reference',help=helpreference)
parser_combinatorial.add_argument('-q', '--query', help=helpquery)
parser_combinatorial.add_argument('-t','--title', default='intersection_test', help=helptitle)
parser_combinatorial.add_argument('-g', type=str, help=helpgroup +" (Default:None)")
parser_combinatorial.add_argument('-c', default="regions", help=helpcolor +' (Default: regions)')
parser_combinatorial.add_argument('-organism',default='hg19', help='Define the organism. (Default: hg19)')
parser_combinatorial.add_argument('-m', default="OVERLAP", choices=['OVERLAP','ORIGINAL','COMP_INCL'], 
                                  help="Define the mode for intersection. \
                                  'OVERLAP' defines the true intersections which are included in both reference and query, \
                                  'ORIGINAL' defines the intersection as the regions of reference which have any intersections with query,\
                                  'COMP_INCL' defines the intersection as the regions of query which are completely included by reference.")
parser_combinatorial.add_argument('-log', action="store_true", help='Set y axis of the plot in log scale.')
parser_combinatorial.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_combinatorial.add_argument('-pdf', action="store_true", help='Save the plot in pdf format.')
parser_combinatorial.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_combinatorial.add_argument('-show', action="store_true", help='Show the figure in the screen.')
################### Boxplot ##########################################

parser_boxplot = subparsers.add_parser('boxplot',help='Boxplot based on the BAM and BED files for gene association analysis.')
parser_boxplot.add_argument('input',help=helpinput)
parser_boxplot.add_argument('output', help=helpoutput)
parser_boxplot.add_argument('-t','--title', default='Boxplot', help=helptitle)
parser_boxplot.add_argument('-g', default='reads', help=helpgroup + " (Default:reads)")
parser_boxplot.add_argument('-c', default='regions', help=helpcolor + " (Default:regions)")
parser_boxplot.add_argument('-s', default='cell', help=helpsort + " (Default:cell)")
parser_boxplot.add_argument('-log', action="store_true", help='Set y axis of the plot in log scale.')
parser_boxplot.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_boxplot.add_argument('-nqn', action="store_true", help='No quantile normalization in calculation.')
parser_boxplot.add_argument('-pdf', action="store_true", help='Save the figure in pdf format.')
parser_boxplot.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_boxplot.add_argument('-p','--pvalue', type=float, default=0.05, help='Define the significance level for multiple test. Default: 0.01')
parser_boxplot.add_argument('-show', action="store_true", help='Show the figure in the screen.')

################### Lineplot ##########################################
parser_lineplot = subparsers.add_parser('lineplot', help='Generate lineplot with various modes.')

choice_center = ['midpoint','leftend','rightend','bothends'] # Be consist as the arguments of GenomicRegionSet.relocate_regions

parser_lineplot.add_argument('input', help=helpinput)
parser_lineplot.add_argument('output', help=helpoutput)
parser_lineplot.add_argument('-t','--title', default='Lineplot', help=helptitle)
parser_lineplot.add_argument('-center', choices=choice_center, default='midpoint', 
                             help='Define the center to calculate coverage on the regions. Options are: '+', '.join(choice_center) + 
                             '.(Default:midpoint) The bothend mode will flap the right end region for calculation.')
parser_lineplot.add_argument('-g', default='reads', help=helpgroup + " (Default:reads)")
parser_lineplot.add_argument('-c', default='regions', help=helpcolor + " (Default:regions)")
parser_lineplot.add_argument('-s', default='cell', help=helpsort + " (Default:cell)")
parser_lineplot.add_argument('-e', type=int, default=2000, help='Define the extend length of interested region for plotting.(Default:2000)')
parser_lineplot.add_argument('-rs', type=int, default=200, help='Define the readsize for calculating coverage.(Default:200)')
parser_lineplot.add_argument('-ss', type=int, default=50, help='Define the stepsize for calculating coverage.(Default:50)')
parser_lineplot.add_argument('-bs', type=int, default=100, help='Define the binsize for calculating coverage.(Default:100)')
parser_lineplot.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_lineplot.add_argument('-pdf', action="store_true", help='Save the figure in pdf format.')
parser_lineplot.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_lineplot.add_argument('-show', action="store_true", help='Show the figure in the screen.')
parser_lineplot.add_argument('-table', action="store_true", help='Store the tables of the figure in text format.')

################### Heatmap ##########################################
parser_heatmap = subparsers.add_parser('heatmap', help='Generate heatmap with various modes.')

choice_center = ['midpoint','leftend','rightend','bothends'] # Be consist as the arguments of GenomicRegionSet.relocate_regions

parser_heatmap.add_argument('input', help=helpinput)
parser_heatmap.add_argument('output', help=helpoutput)
parser_heatmap.add_argument('-t', '--title', default='Heatmap', help=helptitle)
parser_heatmap.add_argument('-center', choices=choice_center, default='midpoint', 
                             help='Define the center to calculate coverage on the regions. Options are: '+', '.join(choice_center) + 
                             '.(Default:midpoint) The bothend mode will flap the right end region for calculation.')
parser_heatmap.add_argument('-sort',type=int, default=None, help='Define the way to sort the signals. \
Default is no sorting at all, the signals arrange in the order of their position; \
"0" is sorting by the average ranking of all signals; \
"1" is sorting by the ranking of 1st column; "2" is 2nd and so on... ')
parser_heatmap.add_argument('-s', default='cell', help=helpsort + " (Default:cell)")
parser_heatmap.add_argument('-g', default='regions', help=helpgroup + " (Default:regions)")
parser_heatmap.add_argument('-c', default='reads', help=helpcolor + " (Default:reads)")
parser_heatmap.add_argument('-e', type=int, default=2000, help='Define the extend length of interested region for plotting.(Default:2000)')
parser_heatmap.add_argument('-rs', type=int, default=200, help='Define the readsize for calculating coverage.(Default:200)')
parser_heatmap.add_argument('-ss', type=int, default=50, help='Define the stepsize for calculating coverage.(Default:50)')
parser_heatmap.add_argument('-bs', type=int, default=100, help='Define the binsize for calculating coverage.(Default:100)')
parser_heatmap.add_argument('-color', action="store_true", help=helpDefinedColot)
parser_heatmap.add_argument('-log', action="store_true", help='Set colorbar in log scale.')
parser_heatmap.add_argument('-pdf', action="store_true", help='Save the figure in pdf format.')
parser_heatmap.add_argument('-html', action="store_true", help='Save the figure in html format.')
parser_heatmap.add_argument('-show', action="store_true", help='Show the figure in the screen.')
parser_heatmap.add_argument('-table', action="store_true", help='Store the tables of the figure in text format.')
################### Integration ##########################################
parser_integration = subparsers.add_parser('integration', help='Provides some tools to deal with experimental matrix or other purposes.')
parser_integration.add_argument('-ihtml', help='Integrate all the html files within the given directory and generate index.html for all plots.')
parser_integration.add_argument('-l2m', help='Convert a given file list in txt format into a experimental matrix.')
parser_integration.add_argument('-output', help='Define the folder of the output file.') 
################### Parsing the arguments ################################
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
elif len(sys.argv) == 2: 
    # retrieve subparsers from parser
    subparsers_actions = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
    # there will probably only be one subparser_action,but better save than sorry
    for subparsers_action in subparsers_actions:
        # get all subparsers and print help
        for choice, subparser in subparsers_action.choices.items():
            if choice == sys.argv[1]:
                print("\nYou need more arguments.")
                print("\nSubparser '{}'".format(choice))        
                subparser.print_help()
    sys.exit(1)
else:
    args = parser.parse_args()
    
#################################################################################################
##### Main #####################################################################################
#################################################################################################

t0 = time.time()
# Input parameters dictionary
parameter = [] 

parameter.append("Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
parameter.append("User: " + getpass.getuser())
try: parameter.append("Project: " + args.output)
except: pass
parameter.append("\nCommand:\n   $ python " + " ".join(sys.argv))
parameter.append("")

################### Projection test ##########################################
if args.mode == 'projection':
    # Fetching reference and query EM
    projection = projection(args.reference,args.query)
    projection.group_refque(args.g)
    projection.colors(args.c, args.color)
    if args.intersect: 
        projection.ref_inter()
        qlist = projection.projection_test(organism = args.organism)
        print2(projection.parameter, "Taking intersect of references as the background. ")
    else:
        qlist = projection.projection_test(organism = args.organism)

    if args.pdf:
        projection.plot(args.log)
        output(f=projection.fig, directory = args.output, folder = args.title, filename="projection_test",extra=plt.gci())
    if args.html:
        projection.gen_html(args.output, args.title)
    if args.table:
        projection.table(directory = args.output, folder = args.title)
    parameter = parameter + projection.parameter
    t1 = time.time()
    print2(parameter,"\nTotal running time is : " + str(datetime.timedelta(seconds=round(t1-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")
        
################### Jaccard test ##########################################
if args.mode == "jaccard":
    """Return the jaccard test of every possible comparisons between two ExperimentalMatrix. 
    
    Method:
    The distribution of random jaccard index is calculated by randomizing query for given times. 
    Then, we compare the real jaccard index to the distribution and formulate p-value as 
    p-value = (# random jaccard > real jaccard)/(# random jaccard)
    
    """
    jaccard = jaccard(args.reference,args.query)
    jaccard.group_refque(args.g)
    jaccard.colors(args.c, args.color)
    
    
    jaccard.jaccard_test(args.runtime, args.organism)
    parameter = parameter + jaccard.parameter
    t1 = time.time()
    if args.pdf:
        jaccard.plot(args.log)
        output(f=jaccard.fig, directory = args.output, folder = args.title, filename="jaccard_test",extra=plt.gci())
    if args.html:
        jaccard.gen_html(args.output, args.title)
    print2(parameter,"\nTotal running time is : " + str(datetime.timedelta(seconds=round(t1-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")
    
################### Intersect Test ##########################################
if args.mode == 'intersection':
    # Fetching reference and query EM
    inter = intersect(args.reference,args.query,mode_intersect = args.m)
    inter.group_refque(args.g)
    inter.colors(args.c, args.color)
    inter.count_intersect()
    
    if args.pdf:
        inter.barplot(args.log)
        output(f=inter.bar, directory = args.output, folder = args.title, filename="intersection_bar",extra=plt.gci())
        if args.stackedbar:
            inter.stackedbar()
            output(f=inter.stackedbar, directory = args.output, folder = args.title, filename="intersection_stackedbar",extra=plt.gci())
        if args.pbar:
            inter.percentagebar()
            output(f=inter.stackedbar, directory = args.output, folder = args.title, filename="intersection_percentagebar",extra=plt.gci())
    if args.html:
        inter.gen_html(args.output, args.title)
    parameter = parameter + inter.parameter
    t1 = time.time()
    print2(parameter,"\nTotal running time is : " + str(datetime.timedelta(seconds=round(t1-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")


################### Combinatorial ##########################################
if args.mode == 'combinatorial':
    comb = combinatorial(args.reference,args.query,mode_intersect = args.m)
    comb.group_refque(args.g)
    comb.resort()
    comb.colors(args.c, args.color)
    sys.exit[0]
    if args.pdf:
        comb.barplot(args.log)
        output(f=inter.bar, directory = args.output, folder = args.title, filename="intersection_bar",extra=plt.gci())
        if args.stackedbar:
            inter.stackedbar()
            output(f=inter.stackedbar, directory = args.output, folder = args.title, filename="intersection_stackedbar",extra=plt.gci())
        if args.pbar:
            inter.percentagebar()
            output(f=inter.stackedbar, directory = args.output, folder = args.title, filename="intersection_percentagebar",extra=plt.gci())
    if args.html:
        inter.gen_html(args.output, args.title)
    parameter = parameter + inter.parameter
    t1 = time.time()
    print2(parameter,"\nTotal running time is : " + str(datetime.timedelta(seconds=round(t1-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")



################### Boxplot ##########################################
if args.mode == 'boxplot':
    exps = ExperimentalMatrix()
    exps.read(args.input)
    boxplot = boxplot(exps, title="Boxplot")
    
    print2(parameter,"\nStep 1/5: Combining all regions")
    all_bed = boxplot.combine_allregions()
    print2(parameter,"    " + str(len(all_bed.sequences)) + " regions from all bed files are combined.")
    t1 = time.time()
    print2(parameter,"    --- finished in {0:.3f} secs\n".format(t1-t0))
    
    # Coverage of reads on all_bed
    print2(parameter,"Step 2/5: Calculating coverage of each bam file on all regions")
    all_table = boxplot.bedCoverage(all_bed) 
    t2 = time.time()
    print2(parameter,"    --- finished in {0:.3f} secs\n".format(t2-t1))
    
    # Quantile normalization
    print2(parameter,"Step 3/5: Quantile normalization of all coverage table")
    if args.nqn:
        print2(parameter,"    No quantile normalization.")
        norm_table = all_table
    else:
        norm_table = boxplot.quantile_normalization(all_table)
    t3 = time.time()
    print2(parameter,"    --- finished in {0:.3f} secs\n".format(t3-t2))
    
    # Generate individual table for each bed
    print2(parameter,"Step 4/5: Constructing different tables for box plot")
    tables = boxplot.tables_for_plot(norm_table,all_bed)
    t4 = time.time()
    print2(parameter,"    --- finished in {0:.3f} secs\n".format(t4-t3))
    
    # Plotting
    print2(parameter,"Step 5/5: Plotting")
    boxplot.group_tags(groupby=args.g, sortby=args.s, colorby=args.c)
    boxplot.group_data(tables=tables)
    boxplot.color_map(colorby=args.c, definedinEM=args.color)
    boxplot.plot(title=args.title,html=args.html, logT=args.log)
    output(f=boxplot.fig, directory = args.output, folder = args.title, filename="boxplot",extra=plt.gci())
    # HTML
    if args.html: boxplot.gen_html(args.output, args.title, args.pvalue)
    t5 = time.time()
    print2(parameter,"    --- finished in {0:.3f} secs\n".format(t5-t4))
    print2(parameter,"Total running time is : " + str(datetime.timedelta(seconds=round(t5-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")

################### Lineplot #########################################
if args.mode == 'lineplot':
    # Read experimental matrix
    t0 = time.time()
    exps = ExperimentalMatrix()
    exps.read(args.input)
    if "reads" not in (args.g, args.c, args.s):
        print("Please add 'reads' tag as one of grouping, sorting, or coloring argument.")
        sys.exit(1)
    if "regions" not in (args.g, args.c, args.s):
        print("Please add 'regions' tag as one of grouping, sorting, or coloring argument.")
        sys.exit(1)
    print2(parameter, "Parameters:\tExtend length:\t"+str(args.e))
    print2(parameter, "\t\tRead size:\t"+str(args.rs))
    print2(parameter, "\t\tBin size:\t"+str(args.bs))
    print2(parameter, "\t\tStep size:\t"+str(args.ss))
    print2(parameter, "\t\tCenter mode:\t"+str(args.center+"\n"))

    lineplot = lineplot(exps, title=args.title, center=args.center, extend=args.e, rs=args.rs, bs=args.bs, ss=args.ss)
    # Processing the regions by given parameters
    print2(parameter, "Step 1/3: Processing regions by given parameters")
    lineplot.relocate_bed()
    t1 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t1-t0))
    
    print2(parameter, "\nStep 2/3: Calculating the coverage to all reads and averaging ")
    lineplot.group_tags(groupby=args.g, sortby=args.s, colorby=args.c)
    lineplot.gen_cues()
    lineplot.coverage(sortby=args.s)
    t2 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t2-t1))
    
    # Plotting
    print2(parameter, "\nStep 3/3: Plotting the lineplots")
    lineplot.colormap(colorby = args.c, definedinEM = args.color)
    lineplot.plot(groupby=args.g, colorby=args.c, output=args.output, printtable=args.table)
    output(f=lineplot.fig, directory = args.output, folder = args.title, filename="lineplot",extra=plt.gci())
    if args.html: lineplot.gen_html(args.output, args.title)
    t3 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t3-t2))
    print2(parameter, "\nTotal running time is : " + str(datetime.timedelta(seconds=round(t3-t0))))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")

################### Heatmap ##########################################
if args.mode=='heatmap':
    # Most part of heat map are the same as lineplot, so it share the same class as lineplot
    # Read experimental matrix
    t0 = time.time()
    exps = ExperimentalMatrix()
    exps.read(args.input)
    if "reads" not in (args.g, args.c, args.s):
        print("Please add 'reads' tag as one of grouping, sorting, or coloring argument.")
        sys.exit(1)
    if "regions" not in (args.g, args.c, args.s):
        print("Please add 'regions' tag as one of grouping, sorting, or coloring argument.")
        sys.exit(1)
    print2(parameter, "Parameters:\tExtend length:\t"+str(args.e))
    print2(parameter, "\t\tRead size:\t"+str(args.rs))
    print2(parameter, "\t\tBin size:\t"+str(args.bs))
    print2(parameter, "\t\tStep size:\t"+str(args.ss))
    print2(parameter, "\t\tCenter mode:\t"+str(args.center+"\n"))

    lineplot = lineplot(exps, title=args.title, center=args.center, extend=args.e, rs=args.rs, bs=args.bs, ss=args.ss)
    # Processing the regions by given parameters
    print2(parameter, "Step 1/4: Processing regions by given parameters")
    lineplot.relocate_bed()
    t1 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t1-t0))
    
    print2(parameter, "\nStep 2/4: Calculating the coverage to all reads and averaging ")
    lineplot.group_tags(groupby=args.g, sortby=args.s, colorby=args.c)
    lineplot.gen_cues()
    lineplot.coverage(sortby=args.s, heatmap=True, logt=args.log)
    t2 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t2-t1))
    
    # Sorting 
    print2(parameter, "\nStep 3/4: Sorting the data for heatmap")
    lineplot.hmsort(sort=args.sort)
    t3 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t3-t2))
    
    # Plotting
    print2(parameter, "\nStep 4/4: Plotting the heatmap")
    lineplot.hmcmlist(colorby = args.c, definedinEM = args.color)
    lineplot.heatmap(args.log)
    for i, name in enumerate(lineplot.hmfiles):
        output(f=lineplot.figs[i], directory = args.output, folder = args.title, filename=name)
    if args.html: lineplot.gen_htmlhm(args.output, args.title)
    t4 = time.time()
    print2(parameter, "    --- finished in {0:.2f} secs".format(t4-t3))
    print2(parameter, "\nTotal running time is : " + str(datetime.timedelta(seconds=t4-t0)))
    output_parameters(parameter, directory = args.output, folder = args.title, filename="parameters.txt")
    
################### Integration ######################################
if args.mode=='integration':
    if args.l2m:
        f1 = open(args.l2m,'r')
        f2 = open(args.output, 'w')
        f2.write("name\ttype\tfile\tfactor")
        for l in f1.readlines():
            f = l.strip()
            name = l.split('.')[0]
            if l.split('.')[1].strip() == "bed":
                ty = "regions"
            elif l.split('.')[1].strip() == "bam":
                ty = "reads"
            f2.write("\n{0}\t{1}\tChIP-Seq_Compendium/{2}\t{3}".format(name, ty, f,name))
        f1.close()
        f2.close()
        
    if args.ihtml:
        directory = args.ihtml
        try:
            os.stat(os.path.join(dir,directory))
        except:
            sys.exit("No such directory.")
        f = open(os.path.join(dir,directory,"index.html"),'w')
        table = []
        # Header
        
        table.append(['<style>table{width:100%;border:1px solid black;border-collapse:collapse;text-align:center;table-layout: fixed;font-size:8pt;}\
            </style><font size="7">' + directory + "</font>"])
        # Each row is a plot with its data
        for root, dirnames, filenames in os.walk(os.path.join(dir,directory)):
            for filename in fnmatch.filter(filenames, '*.html'):
                if filename != 'index.html':
                    table.append(["<a href='"+os.path.join(root, filename)+"'><font size="+'"5"'+">"+root.split('/')[-1]+"</a>"])
        htmlcode = HTML.table(table)
        for line in htmlcode: f.write(line)
        f.close()
        sys.exit("Integration finished.")