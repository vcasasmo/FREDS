
% Increase counter:

if (exist('idx', 'var'));
  idx = idx + 1;
else;
  idx = 1;
end;

% Version, title and date:

VERSION                   (idx, [1:  13]) = 'Serpent 2.2.1' ;
COMPILE_DATE              (idx, [1:  20]) = 'Sep 28 2023 07:42:40' ;
DEBUG                     (idx, 1)        = 0 ;
TITLE                     (idx, [1:   8]) = 'Untitled' ;
CONFIDENTIAL_DATA         (idx, 1)        = 0 ;
INPUT_FILE_NAME           (idx, [1:   4]) = 'main' ;
WORKING_DIRECTORY         (idx, [1:  25]) = '/home/aimetta/GA_SCK/xGPT' ;
HOSTNAME                  (idx, [1:  11]) = 'blanketcool' ;
CPU_TYPE                  (idx, [1:  35]) = 'Intel Xeon Processor (Skylake, IBRS' ;
CPU_MHZ                   (idx, 1)        = 1.0 ;
START_DATE                (idx, [1:  24]) = 'Tue Mar 19 16:20:13 2024' ;
COMPLETE_DATE             (idx, [1:  24]) = 'Sun Mar 24 08:30:37 2024' ;

% Run parameters:

POP                       (idx, 1)        = 1000000 ;
CYCLES                    (idx, 1)        = 1000 ;
SKIP                      (idx, 1)        = 50 ;
BATCH_INTERVAL            (idx, 1)        = 25 ;
SRC_NORM_MODE             (idx, 1)        = 2 ;
SEED                      (idx, 1)        = 1710865213556 ;
UFS_MODE                  (idx, 1)        = 0 ;
UFS_ORDER                 (idx, 1)        = 1.00000 ;
NEUTRON_TRANSPORT_MODE    (idx, 1)        = 1 ;
PHOTON_TRANSPORT_MODE     (idx, 1)        = 0 ;
GROUP_CONSTANT_GENERATION (idx, 1)        = 0 ;
B1_CALCULATION            (idx, [1:  3])  = [ 0 0 0 ] ;
B1_IMPLICIT_LEAKAGE       (idx, 1)        = 0 ;
B1_BURNUP_CORRECTION      (idx, 1)        = 0 ;

CRIT_SPEC_MODE            (idx, 1)        = 0 ;
IMPLICIT_REACTION_RATES   (idx, 1)        = 1 ;

% Optimization:

OPTIMIZATION_MODE         (idx, 1)        = 4 ;
RECONSTRUCT_MICROXS       (idx, 1)        = 1 ;
RECONSTRUCT_MACROXS       (idx, 1)        = 1 ;
DOUBLE_INDEXING           (idx, 1)        = 0 ;
MG_MAJORANT_MODE          (idx, 1)        = 0 ;

% Parallelization:

MPI_TASKS                 (idx, 1)        = 1 ;
OMP_THREADS               (idx, 1)        = 30 ;
MPI_REPRODUCIBILITY       (idx, 1)        = 0 ;
OMP_REPRODUCIBILITY       (idx, 1)        = 1 ;
OMP_HISTORY_PROFILE       (idx, [1:  30]) = [  1.10893E+00  1.02259E+00  9.54735E-01  9.95028E-01  9.57680E-01  1.01573E+00  9.81071E-01  9.74749E-01  9.96346E-01  9.65895E-01  9.77047E-01  9.62242E-01  1.00681E+00  1.06687E+00  1.00441E+00  1.03962E+00  1.07770E+00  9.94540E-01  9.60219E-01  1.01855E+00  1.01449E+00  9.24343E-01  9.33922E-01  1.01076E+00  9.84278E-01  1.00299E+00  1.02512E+00  9.67033E-01  9.66599E-01  1.08970E+00  ];
SHARE_BUF_ARRAY           (idx, 1)        = 0 ;
SHARE_RES2_ARRAY          (idx, 1)        = 1 ;
OMP_SHARED_QUEUE_LIM      (idx, 1)        = 0 ;

% File paths:

XS_DATA_FILE_PATH         (idx, [1:  45]) = '/opt/serpent/xsdata/endfb8/sss2_endfb8.xsdata' ;
DECAY_DATA_FILE_PATH      (idx, [1:   3]) = 'N/A' ;
SFY_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;
NFY_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;
BRA_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;

% Collision and reaction sampling (neutrons/photons):

MIN_MACROXS               (idx, [1:   4]) = [  5.00000E-02 0.0E+00  0.00000E+00 0.0E+00 ];
DT_THRESH                 (idx, [1:   2]) = [  9.00000E-01  9.00000E-01 ] ;
ST_FRAC                   (idx, [1:   4]) = [  9.72731E-02 6.3E-05  0.00000E+00 0.0E+00 ];
DT_FRAC                   (idx, [1:   4]) = [  9.02727E-01 6.8E-06  0.00000E+00 0.0E+00 ];
DT_EFF                    (idx, [1:   4]) = [  2.93955E-01 8.0E-06  0.00000E+00 0.0E+00 ];
REA_SAMPLING_EFF          (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
REA_SAMPLING_FAIL         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_COL_EFF               (idx, [1:   4]) = [  1.54514E-01 5.7E-06  0.00000E+00 0.0E+00 ];
AVG_TRACKING_LOOPS        (idx, [1:   8]) = [  7.63570E+00 2.8E-05  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
CELL_SEARCH_FRAC          (idx, [1:  10]) = [  9.78385E-01 4.9E-07  2.13963E-02 2.2E-05  2.18433E-04 0.00010  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
AVG_TRACKS                (idx, [1:   4]) = [  5.92563E+03 0.00030  0.00000E+00 0.0E+00 ];
AVG_REAL_COL              (idx, [1:   4]) = [  5.92487E+03 0.00030  0.00000E+00 0.0E+00 ];
AVG_VIRT_COL              (idx, [1:   4]) = [  1.32477E+04 0.00030  0.00000E+00 0.0E+00 ];
AVG_SURF_CROSS            (idx, [1:   4]) = [  1.59211E+03 0.00031  0.00000E+00 0.0E+00 ];
LOST_PARTICLES            (idx, 1)        = 0 ;

% Run statistics:

CYCLE_IDX                 (idx, 1)        = 1000 ;
SIMULATED_HISTORIES       (idx, 1)        = 1000049633 ;
MEAN_POP_SIZE             (idx, [1:   2]) = [  1.00005E+06 0.00006 ] ;
MEAN_POP_WGT              (idx, [1:   2]) = [  1.00005E+06 0.00006 ] ;
SIMULATION_COMPLETED      (idx, 1)        = 1 ;

% Running times:

TOT_CPU_TIME              (idx, 1)        =  1.36701E+05 ;
RUNNING_TIME              (idx, 1)        =  6.73040E+03 ;
INIT_TIME                 (idx, [1:   2]) = [  1.76293E+00  1.76293E+00 ] ;
PROCESS_TIME              (idx, [1:   2]) = [  2.01667E-02  2.01667E-02 ] ;
TRANSPORT_CYCLE_TIME      (idx, [1:   3]) = [  6.72862E+03  6.72862E+03  0.00000E+00 ] ;
MPI_OVERHEAD_TIME         (idx, [1:   2]) = [  0.00000E+00  0.00000E+00 ] ;
ESTIMATED_RUNNING_TIME    (idx, [1:   2]) = [  6.73040E+03  0.00000E+00 ] ;
CPU_USAGE                 (idx, 1)        = 20.31096 ;
TRANSPORT_CPU_USAGE       (idx, [1:   2]) = [  2.03594E+01 0.00179 ];
OMP_PARALLEL_FRAC         (idx, 1)        =  6.70959E-01 ;

% Memory usage:

AVAIL_MEM                 (idx, 1)        = 128827.30 ;
ALLOC_MEMSIZE             (idx, 1)        = 89867.15 ;
MEMSIZE                   (idx, 1)        = 89641.48 ;
XS_MEMSIZE                (idx, 1)        = 6922.32 ;
MAT_MEMSIZE               (idx, 1)        = 621.74 ;
RES_MEMSIZE               (idx, 1)        = 126.07 ;
IFC_MEMSIZE               (idx, 1)        = 0.00 ;
MISC_MEMSIZE              (idx, 1)        = 53407.49 ;
UNKNOWN_MEMSIZE           (idx, 1)        = 28563.85 ;
UNUSED_MEMSIZE            (idx, 1)        = 225.67 ;

% Geometry parameters:

TOT_CELLS                 (idx, 1)        = 200 ;
UNION_CELLS               (idx, 1)        = 0 ;

% Neutron energy grid:

NEUTRON_ERG_TOL           (idx, 1)        =  0.00000E+00 ;
NEUTRON_ERG_NE            (idx, 1)        = 1042278 ;
NEUTRON_EMIN              (idx, 1)        =  1.00000E-11 ;
NEUTRON_EMAX              (idx, 1)        =  2.00000E+01 ;

% Unresolved resonance probability table sampling:

URES_DILU_CUT             (idx, 1)        =  1.00000E-09 ;
URES_EMIN                 (idx, 1)        =  1.50000E-04 ;
URES_EMAX                 (idx, 1)        =  3.00000E+00 ;
URES_AVAIL                (idx, 1)        = 31 ;
URES_USED                 (idx, 1)        = 31 ;

% Nuclides and reaction channels:

TOT_NUCLIDES              (idx, 1)        = 76 ;
TOT_TRANSPORT_NUCLIDES    (idx, 1)        = 76 ;
TOT_DOSIMETRY_NUCLIDES    (idx, 1)        = 0 ;
TOT_DECAY_NUCLIDES        (idx, 1)        = 0 ;
TOT_PHOTON_NUCLIDES       (idx, 1)        = 0 ;
TOT_REA_CHANNELS          (idx, 1)        = 2408 ;
TOT_TRANSMU_REA           (idx, 1)        = 0 ;

% Neutron physics options:

USE_DELNU                 (idx, 1)        = 1 ;
USE_URES                  (idx, 1)        = 1 ;
USE_DBRC                  (idx, 1)        = 0 ;
IMPL_CAPT                 (idx, 1)        = 0 ;
IMPL_NXN                  (idx, 1)        = 1 ;
IMPL_FISS                 (idx, 1)        = 0 ;
DOPPLER_PREPROCESSOR      (idx, 1)        = 1 ;
TMS_MODE                  (idx, 1)        = 0 ;
SAMPLE_FISS               (idx, 1)        = 1 ;
SAMPLE_CAPT               (idx, 1)        = 1 ;
SAMPLE_SCATT              (idx, 1)        = 1 ;

% Energy deposition:

EDEP_MODE                 (idx, 1)        = 0 ;
EDEP_DELAYED              (idx, 1)        = 1 ;
EDEP_KEFF_CORR            (idx, 1)        = 1 ;
EDEP_LOCAL_EGD            (idx, 1)        = 0 ;
EDEP_COMP                 (idx, [1:   9]) = [ 0 0 0 0 0 0 0 0 0 ] ;
EDEP_CAPT_E               (idx, 1)        =  0.00000E+00 ;

% Radioactivity data:

TOT_ACTIVITY              (idx, 1)        =  0.00000E+00 ;
TOT_DECAY_HEAT            (idx, 1)        =  0.00000E+00 ;
TOT_SF_RATE               (idx, 1)        =  0.00000E+00 ;
ACTINIDE_ACTIVITY         (idx, 1)        =  0.00000E+00 ;
ACTINIDE_DECAY_HEAT       (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_ACTIVITY  (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_DECAY_HEAT(idx, 1)        =  0.00000E+00 ;
INHALATION_TOXICITY       (idx, 1)        =  0.00000E+00 ;
INGESTION_TOXICITY        (idx, 1)        =  0.00000E+00 ;
ACTINIDE_INH_TOX          (idx, 1)        =  0.00000E+00 ;
ACTINIDE_ING_TOX          (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_INH_TOX   (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_ING_TOX   (idx, 1)        =  0.00000E+00 ;
SR90_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
TE132_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
I131_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
I132_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
CS134_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
CS137_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
PHOTON_DECAY_SOURCE       (idx, [1:   2]) = [  0.00000E+00  0.00000E+00 ] ;
NEUTRON_DECAY_SOURCE      (idx, 1)        =  0.00000E+00 ;
ALPHA_DECAY_SOURCE        (idx, 1)        =  0.00000E+00 ;
ELECTRON_DECAY_SOURCE     (idx, 1)        =  0.00000E+00 ;

% Normalization coefficient:

NORM_COEF                 (idx, [1:   4]) = [  3.99088E-08 2.9E-05  0.00000E+00 0.0E+00 ];

% Analog reaction rate estimators:

CONVERSION_RATIO          (idx, [1:   2]) = [  6.39312E-01 9.0E-05 ];
U235_FISS                 (idx, [1:   4]) = [  5.74093E-03 0.00040  1.57175E-02 0.00041 ];
U238_FISS                 (idx, [1:   4]) = [  3.08555E-02 0.00020  8.44758E-02 0.00019 ];
PU239_FISS                (idx, [1:   4]) = [  2.52571E-01 6.6E-05  6.91485E-01 3.2E-05 ];
PU240_FISS                (idx, [1:   4]) = [  2.63444E-02 0.00020  7.21255E-02 0.00020 ];
PU241_FISS                (idx, [1:   4]) = [  3.71544E-02 0.00017  1.01721E-01 0.00015 ];
U235_CAPT                 (idx, [1:   4]) = [  1.61308E-03 0.00075  2.66877E-03 0.00074 ];
U238_CAPT                 (idx, [1:   4]) = [  2.00821E-01 7.4E-05  3.32249E-01 6.6E-05 ];
PU239_CAPT                (idx, [1:   4]) = [  6.62417E-02 0.00010  1.09594E-01 0.00010 ];
PU240_CAPT                (idx, [1:   4]) = [  3.19346E-02 0.00019  5.28343E-02 0.00018 ];
PU241_CAPT                (idx, [1:   4]) = [  6.37677E-03 0.00039  1.05501E-02 0.00040 ];

% Neutron balance (particles/weight):

BALA_SRC_NEUTRON_SRC      (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_SRC_NEUTRON_FISS     (idx, [1:   2]) = [ 1000049633 1.00000E+09 ] ;
BALA_SRC_NEUTRON_NXN      (idx, [1:   2]) = [ 0 2.30541E+06 ] ;
BALA_SRC_NEUTRON_VR       (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_SRC_NEUTRON_TOT      (idx, [1:   2]) = [ 1000049633 1.00231E+09 ] ;

BALA_LOSS_NEUTRON_CAPT    (idx, [1:   2]) = [ 604358128 6.05811E+08 ] ;
BALA_LOSS_NEUTRON_FISS    (idx, [1:   2]) = [ 365352265 3.66093E+08 ] ;
BALA_LOSS_NEUTRON_LEAK    (idx, [1:   2]) = [ 30339240 3.04021E+07 ] ;
BALA_LOSS_NEUTRON_CUT     (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_LOSS_NEUTRON_ERR     (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_LOSS_NEUTRON_TOT     (idx, [1:   2]) = [ 1000049633 1.00231E+09 ] ;

BALA_NEUTRON_DIFF         (idx, [1:   2]) = [ 0 2.97413E-02 ] ;

% Normalized total reaction rates (neutrons):

TOT_POWER                 (idx, [1:   2]) = [  1.21746E-11 2.1E-05 ];
TOT_POWDENS               (idx, [1:   2]) = [  9.99266E-20 2.1E-05 ];
TOT_GENRATE               (idx, [1:   2]) = [  1.07032E+00 2.1E-05 ];
TOT_FISSRATE              (idx, [1:   2]) = [  3.65225E-01 2.1E-05 ];
TOT_CAPTRATE              (idx, [1:   2]) = [  6.04443E-01 1.3E-05 ];
TOT_ABSRATE               (idx, [1:   2]) = [  9.69667E-01 6.6E-06 ];
TOT_SRCRATE               (idx, [1:   2]) = [  9.97721E-01 2.9E-05 ];
TOT_FLUX                  (idx, [1:   2]) = [  3.58570E+02 3.4E-05 ];
TOT_PHOTON_PRODRATE       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_LEAKRATE              (idx, [1:   2]) = [  3.03328E-02 0.00021 ];
ALBEDO_LEAKRATE           (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_LOSSRATE              (idx, [1:   2]) = [  1.00000E+00 0.0E+00 ];
TOT_CUTRATE               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_RR                    (idx, [1:   2]) = [  1.18457E+02 3.6E-05 ];
INI_FMASS                 (idx, 1)        =  1.21836E+02 ;
TOT_FMASS                 (idx, 1)        =  1.21836E+02 ;

% Six-factor formula:

SIX_FF_ETA                (idx, [1:   2]) = [  1.43874E+00 0.00370 ];
SIX_FF_F                  (idx, [1:   2]) = [  2.15957E-02 0.00332 ];
SIX_FF_P                  (idx, [1:   2]) = [  3.72758E-03 0.00039 ];
SIX_FF_EPSILON            (idx, [1:   2]) = [  9.56273E+03 0.00477 ];
SIX_FF_LF                 (idx, [1:   2]) = [  9.69700E-01 6.7E-06 ];
SIX_FF_LT                 (idx, [1:   2]) = [  9.99895E-01 3.0E-07 ];
SIX_FF_KINF               (idx, [1:   2]) = [  1.10651E+00 3.8E-05 ];
SIX_FF_KEFF               (idx, [1:   2]) = [  1.07287E+00 3.9E-05 ];

% Fission neutron and energy production:

NUBAR                     (idx, [1:   2]) = [  2.93059E+00 9.6E-07 ];
FISSE                     (idx, [1:   2]) = [  2.08059E+02 3.2E-08 ];

% Criticality eigenvalues:

ANA_KEFF                  (idx, [1:   6]) = [  1.07288E+00 4.0E-05  1.06937E+00 3.9E-05  3.49418E-03 0.00089 ];
IMP_KEFF                  (idx, [1:   2]) = [  1.07280E+00 2.1E-05 ];
COL_KEFF                  (idx, [1:   2]) = [  1.07277E+00 3.4E-05 ];
ABS_KEFF                  (idx, [1:   2]) = [  1.07280E+00 2.1E-05 ];
ABS_KINF                  (idx, [1:   2]) = [  1.10643E+00 2.0E-05 ];
GEOM_ALBEDO               (idx, [1:   6]) = [  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00 ];

% ALF (Average lethargy of neutrons causing fission):
% Based on E0 = 2.000000E+01 MeV

ANA_ALF                   (idx, [1:   2]) = [  5.01763E+00 2.6E-05 ];
IMP_ALF                   (idx, [1:   2]) = [  5.01754E+00 1.9E-05 ];

% EALF (Energy corresponding to average lethargy of neutrons causing fission):

ANA_EALF                  (idx, [1:   2]) = [  1.32404E-01 0.00013 ];
IMP_EALF                  (idx, [1:   2]) = [  1.32416E-01 9.4E-05 ];

% AFGE (Average energy of neutrons causing fission):

ANA_AFGE                  (idx, [1:   2]) = [  6.98465E-01 9.4E-05 ];
IMP_AFGE                  (idx, [1:   2]) = [  6.98573E-01 4.3E-05 ];

% Forward-weighted delayed neutron parameters:

PRECURSOR_GROUPS          (idx, 1)        = 6 ;
FWD_ANA_BETA_ZERO         (idx, [1:  14]) = [  3.49945E-03 0.00043  8.90511E-05 0.00346  6.75498E-04 0.00105  5.40117E-04 0.00137  1.23074E-03 0.00074  7.12100E-04 0.00109  2.51947E-04 0.00171 ];
FWD_ANA_LAMBDA            (idx, [1:  14]) = [  5.22388E-01 0.00062  1.33817E-02 3.6E-05  3.08077E-02 1.9E-05  1.16995E-01 4.0E-05  3.06721E-01 3.6E-05  8.78054E-01 3.8E-05  2.93761E+00 0.00010 ];

% Beta-eff using Meulekamp's method:

ADJ_MEULEKAMP_BETA_EFF    (idx, [1:  14]) = [  3.29075E-03 0.00066  8.20901E-05 0.00484  6.39836E-04 0.00117  5.00253E-04 0.00202  1.16269E-03 0.00106  6.68216E-04 0.00136  2.37665E-04 0.00236 ];
ADJ_MEULEKAMP_LAMBDA      (idx, [1:  14]) = [  5.23124E-01 0.00081  1.33833E-02 5.2E-05  3.08074E-02 2.5E-05  1.17032E-01 5.9E-05  3.06857E-01 5.0E-05  8.78221E-01 4.9E-05  2.93898E+00 0.00011 ];

% Adjoint weighted time constants using Nauchi's method:

IFP_CHAIN_LENGTH          (idx, 1)        = 15 ;
ADJ_NAUCHI_GEN_TIME       (idx, [1:   6]) = [  6.71679E-07 0.00040  6.71041E-07 0.00040  8.66644E-07 0.00422 ];
ADJ_NAUCHI_LIFETIME       (idx, [1:   6]) = [  7.20545E-07 0.00038  7.19861E-07 0.00038  9.29695E-07 0.00422 ];
ADJ_NAUCHI_BETA_EFF       (idx, [1:  14]) = [  3.25658E-03 0.00089  8.16952E-05 0.00600  6.34212E-04 0.00231  4.94590E-04 0.00236  1.15024E-03 0.00132  6.60645E-04 0.00208  2.35193E-04 0.00286 ];
ADJ_NAUCHI_LAMBDA         (idx, [1:  14]) = [  5.22876E-01 0.00118  1.33845E-02 7.0E-05  3.08085E-02 3.8E-05  1.17018E-01 8.6E-05  3.06870E-01 6.3E-05  8.78278E-01 5.6E-05  2.93823E+00 0.00019 ];

% Adjoint weighted time constants using IFP:

ADJ_IFP_GEN_TIME          (idx, [1:   6]) = [  6.33005E-07 0.00079  6.32352E-07 0.00078  8.32507E-07 0.01858 ];
ADJ_IFP_LIFETIME          (idx, [1:   6]) = [  6.79058E-07 0.00075  6.78357E-07 0.00075  8.93059E-07 0.01856 ];
ADJ_IFP_IMP_BETA_EFF      (idx, [1:  14]) = [  3.26377E-03 0.00294  8.32881E-05 0.01535  6.30304E-04 0.00623  4.94415E-04 0.00818  1.15564E-03 0.00495  6.63662E-04 0.00689  2.36465E-04 0.01097 ];
ADJ_IFP_IMP_LAMBDA        (idx, [1:  14]) = [  5.24467E-01 0.00445  1.33840E-02 0.00025  3.08109E-02 0.00012  1.17039E-01 0.00031  3.06990E-01 0.00023  8.78798E-01 0.00017  2.93972E+00 0.00053 ];
ADJ_IFP_ANA_BETA_EFF      (idx, [1:  14]) = [  3.26500E-03 0.00298  8.35601E-05 0.01519  6.30892E-04 0.00623  4.95462E-04 0.00810  1.15533E-03 0.00485  6.63454E-04 0.00696  2.36304E-04 0.01040 ];
ADJ_IFP_ANA_LAMBDA        (idx, [1:  14]) = [  5.24079E-01 0.00428  1.33844E-02 0.00025  3.08105E-02 0.00012  1.17035E-01 0.00031  3.06990E-01 0.00024  8.78775E-01 0.00017  2.93954E+00 0.00054 ];
ADJ_IFP_ROSSI_ALPHA       (idx, [1:   2]) = [ -5.16138E+03 0.00294 ];

% Adjoint weighted time constants using perturbation technique:

ADJ_PERT_GEN_TIME         (idx, [1:   2]) = [  6.53536E-07 0.00047 ];
ADJ_PERT_LIFETIME         (idx, [1:   2]) = [  7.01082E-07 0.00043 ];
ADJ_PERT_BETA_EFF         (idx, [1:   2]) = [  3.27236E-03 0.00146 ];
ADJ_PERT_ROSSI_ALPHA      (idx, [1:   2]) = [ -5.00720E+03 0.00152 ];

% Inverse neutron speed :

ANA_INV_SPD               (idx, [1:   2]) = [  1.45664E-08 0.00011 ];

% Analog slowing-down and thermal neutron lifetime (total/prompt/delayed):

ANA_SLOW_TIME             (idx, [1:   6]) = [  1.62287E-04 0.00018  1.62288E-04 0.00018  1.61867E-04 0.00248 ];
ANA_THERM_TIME            (idx, [1:   6]) = [  7.69516E-05 0.00049  7.69549E-05 0.00050  7.60628E-05 0.01042 ];
ANA_THERM_FRAC            (idx, [1:   6]) = [  4.16403E-03 0.00040  4.16374E-03 0.00041  4.24599E-03 0.00728 ];
ANA_DELAYED_EMTIME        (idx, [1:   2]) = [  1.08839E+01 0.00108 ];
ANA_MEAN_NCOL             (idx, [1:   4]) = [  2.36900E+02 3.7E-05  1.11185E+02 6.4E-05 ];

