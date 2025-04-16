
% Increase counter:

if (exist('idx', 'var'));
  idx = idx + 1;
else;
  idx = 1;
end;

% Version, title and date:

VERSION                   (idx, [1:  13]) = 'Serpent 2.2.1' ;
COMPILE_DATE              (idx, [1:  20]) = 'Sep 29 2023 09:48:05' ;
DEBUG                     (idx, 1)        = 0 ;
TITLE                     (idx, [1:   8]) = 'Untitled' ;
CONFIDENTIAL_DATA         (idx, 1)        = 0 ;
INPUT_FILE_NAME           (idx, [1:  18]) = 'FC_Tf_1073_Tc_1073' ;
WORKING_DIRECTORY         (idx, [1:  73]) = '/home/aaimetta/GA_SCK/xGPT/U-238_jeff33_basfun_singlematrices_truncer1e-6' ;
HOSTNAME                  (idx, [1:  11]) = 'compute-4-8' ;
CPU_TYPE                  (idx, [1:  40]) = 'Intel(R) Xeon(R) Gold 6326 CPU @ 2.90GHz' ;
CPU_MHZ                   (idx, 1)        = 218104675.0 ;
START_DATE                (idx, [1:  24]) = 'Fri Apr  5 15:34:06 2024' ;
COMPLETE_DATE             (idx, [1:  24]) = 'Wed Apr 10 04:04:16 2024' ;

% Run parameters:

POP                       (idx, 1)        = 1000000 ;
CYCLES                    (idx, 1)        = 1000 ;
SKIP                      (idx, 1)        = 50 ;
BATCH_INTERVAL            (idx, 1)        = 25 ;
SRC_NORM_MODE             (idx, 1)        = 2 ;
SEED                      (idx, 1)        = 1712324046872 ;
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
OMP_HISTORY_PROFILE       (idx, [1:  30]) = [  1.30918E+00  9.70559E-01  9.26947E-01  9.21026E-01  9.77800E-01  1.05274E+00  9.52156E-01  1.03310E+00  9.52435E-01  1.02394E+00  9.95102E-01  1.04028E+00  9.94079E-01  1.05673E+00  9.25749E-01  9.86969E-01  1.02838E+00  9.82868E-01  1.00090E+00  1.04250E+00  1.02545E+00  9.13649E-01  1.04434E+00  9.06966E-01  9.91717E-01  1.00256E+00  1.02511E+00  9.99080E-01  9.16527E-01  1.00115E+00  ];
SHARE_BUF_ARRAY           (idx, 1)        = 0 ;
SHARE_RES2_ARRAY          (idx, 1)        = 1 ;
OMP_SHARED_QUEUE_LIM      (idx, 1)        = 0 ;

% File paths:

XS_DATA_FILE_PATH         (idx, [1:  59]) = '/home/aaimetta/opt/serpent/xsdata/endfb8/sss2_endfb8.xsdata' ;
DECAY_DATA_FILE_PATH      (idx, [1:   3]) = 'N/A' ;
SFY_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;
NFY_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;
BRA_DATA_FILE_PATH        (idx, [1:   3]) = 'N/A' ;

% Collision and reaction sampling (neutrons/photons):

MIN_MACROXS               (idx, [1:   4]) = [  5.00000E-02 0.0E+00  0.00000E+00 0.0E+00 ];
DT_THRESH                 (idx, [1:   2]) = [  9.00000E-01  9.00000E-01 ] ;
ST_FRAC                   (idx, [1:   4]) = [  9.72783E-02 5.9E-05  0.00000E+00 0.0E+00 ];
DT_FRAC                   (idx, [1:   4]) = [  9.02722E-01 6.3E-06  0.00000E+00 0.0E+00 ];
DT_EFF                    (idx, [1:   4]) = [  2.93956E-01 7.0E-06  0.00000E+00 0.0E+00 ];
REA_SAMPLING_EFF          (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
REA_SAMPLING_FAIL         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_COL_EFF               (idx, [1:   4]) = [  1.54516E-01 7.0E-06  0.00000E+00 0.0E+00 ];
AVG_TRACKING_LOOPS        (idx, [1:   8]) = [  7.63497E+00 3.2E-05  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
CELL_SEARCH_FRAC          (idx, [1:  10]) = [  9.78386E-01 3.6E-07  2.13955E-02 1.7E-05  2.18510E-04 5.4E-05  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
AVG_TRACKS                (idx, [1:   4]) = [  5.92738E+03 0.00025  0.00000E+00 0.0E+00 ];
AVG_REAL_COL              (idx, [1:   4]) = [  5.92662E+03 0.00025  0.00000E+00 0.0E+00 ];
AVG_VIRT_COL              (idx, [1:   4]) = [  1.32514E+04 0.00025  0.00000E+00 0.0E+00 ];
AVG_SURF_CROSS            (idx, [1:   4]) = [  1.59264E+03 0.00025  0.00000E+00 0.0E+00 ];
LOST_PARTICLES            (idx, 1)        = 0 ;

% Run statistics:

CYCLE_IDX                 (idx, 1)        = 1000 ;
SIMULATED_HISTORIES       (idx, 1)        = 1000046377 ;
MEAN_POP_SIZE             (idx, [1:   2]) = [  1.00005E+06 0.00006 ] ;
MEAN_POP_WGT              (idx, [1:   2]) = [  1.00005E+06 0.00006 ] ;
SIMULATION_COMPLETED      (idx, 1)        = 1 ;

% Running times:

TOT_CPU_TIME              (idx, 1)        =  1.26444E+05 ;
RUNNING_TIME              (idx, 1)        =  6.51017E+03 ;
INIT_TIME                 (idx, [1:   2]) = [  9.90850E-01  9.90850E-01 ] ;
PROCESS_TIME              (idx, [1:   2]) = [  1.65833E-02  1.65833E-02 ] ;
TRANSPORT_CYCLE_TIME      (idx, [1:   3]) = [  6.50916E+03  6.50916E+03  0.00000E+00 ] ;
MPI_OVERHEAD_TIME         (idx, [1:   2]) = [  0.00000E+00  0.00000E+00 ] ;
ESTIMATED_RUNNING_TIME    (idx, [1:   2]) = [  6.51016E+03  0.00000E+00 ] ;
CPU_USAGE                 (idx, 1)        = 19.42254 ;
TRANSPORT_CPU_USAGE       (idx, [1:   2]) = [  1.94166E+01 0.00151 ];
OMP_PARALLEL_FRAC         (idx, 1)        =  6.56827E-01 ;

% Memory usage:

AVAIL_MEM                 (idx, 1)        = 515277.81 ;
ALLOC_MEMSIZE             (idx, 1)        = 105564.80 ;
MEMSIZE                   (idx, 1)        = 105289.17 ;
XS_MEMSIZE                (idx, 1)        = 6922.42 ;
MAT_MEMSIZE               (idx, 1)        = 621.74 ;
RES_MEMSIZE               (idx, 1)        = 64.42 ;
IFC_MEMSIZE               (idx, 1)        = 0.00 ;
MISC_MEMSIZE              (idx, 1)        = 53407.49 ;
UNKNOWN_MEMSIZE           (idx, 1)        = 44273.11 ;
UNUSED_MEMSIZE            (idx, 1)        = 275.63 ;

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

NORM_COEF                 (idx, [1:   4]) = [  3.99073E-08 2.9E-05  0.00000E+00 0.0E+00 ];

% Analog reaction rate estimators:

CONVERSION_RATIO          (idx, [1:   2]) = [  6.39331E-01 9.0E-05 ];
U235_FISS                 (idx, [1:   4]) = [  5.73906E-03 0.00040  1.57131E-02 0.00037 ];
U238_FISS                 (idx, [1:   4]) = [  3.08608E-02 0.00016  8.44944E-02 0.00016 ];
PU239_FISS                (idx, [1:   4]) = [  2.52547E-01 7.3E-05  6.91453E-01 3.7E-05 ];
PU240_FISS                (idx, [1:   4]) = [  2.63445E-02 0.00022  7.21290E-02 0.00021 ];
PU241_FISS                (idx, [1:   4]) = [  3.71569E-02 0.00015  1.01733E-01 0.00015 ];
U235_CAPT                 (idx, [1:   4]) = [  1.61346E-03 0.00079  2.66941E-03 0.00078 ];
U238_CAPT                 (idx, [1:   4]) = [  2.00820E-01 8.2E-05  3.32251E-01 6.1E-05 ];
PU239_CAPT                (idx, [1:   4]) = [  6.62439E-02 0.00012  1.09598E-01 0.00012 ];
PU240_CAPT                (idx, [1:   4]) = [  3.19318E-02 0.00013  5.28301E-02 0.00013 ];
PU241_CAPT                (idx, [1:   4]) = [  6.37716E-03 0.00040  1.05508E-02 0.00040 ];

% Neutron balance (particles/weight):

BALA_SRC_NEUTRON_SRC      (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_SRC_NEUTRON_FISS     (idx, [1:   2]) = [ 1000046377 1.00000E+09 ] ;
BALA_SRC_NEUTRON_NXN      (idx, [1:   2]) = [ 0 2.30602E+06 ] ;
BALA_SRC_NEUTRON_VR       (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_SRC_NEUTRON_TOT      (idx, [1:   2]) = [ 1000046377 1.00231E+09 ] ;

BALA_LOSS_NEUTRON_CAPT    (idx, [1:   2]) = [ 604372288 6.05828E+08 ] ;
BALA_LOSS_NEUTRON_FISS    (idx, [1:   2]) = [ 365347847 3.66089E+08 ] ;
BALA_LOSS_NEUTRON_LEAK    (idx, [1:   2]) = [ 30326242 3.03891E+07 ] ;
BALA_LOSS_NEUTRON_CUT     (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_LOSS_NEUTRON_ERR     (idx, [1:   2]) = [ 0 0.00000E+00 ] ;
BALA_LOSS_NEUTRON_TOT     (idx, [1:   2]) = [ 1000046377 1.00231E+09 ] ;

BALA_NEUTRON_DIFF         (idx, [1:   2]) = [ 0 1.24283E-02 ] ;

% Normalized total reaction rates (neutrons):

TOT_POWER                 (idx, [1:   2]) = [  1.21748E-11 2.2E-05 ];
TOT_POWDENS               (idx, [1:   2]) = [  9.99278E-20 2.2E-05 ];
TOT_GENRATE               (idx, [1:   2]) = [  1.07034E+00 2.2E-05 ];
TOT_FISSRATE              (idx, [1:   2]) = [  3.65229E-01 2.2E-05 ];
TOT_CAPTRATE              (idx, [1:   2]) = [  6.04452E-01 1.3E-05 ];
TOT_ABSRATE               (idx, [1:   2]) = [  9.69681E-01 7.9E-06 ];
TOT_SRCRATE               (idx, [1:   2]) = [  9.97684E-01 2.9E-05 ];
TOT_FLUX                  (idx, [1:   2]) = [  3.58568E+02 2.6E-05 ];
TOT_PHOTON_PRODRATE       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_LEAKRATE              (idx, [1:   2]) = [  3.03187E-02 0.00025 ];
ALBEDO_LEAKRATE           (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_LOSSRATE              (idx, [1:   2]) = [  1.00000E+00 0.0E+00 ];
TOT_CUTRATE               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_RR                    (idx, [1:   2]) = [  1.18457E+02 2.6E-05 ];
INI_FMASS                 (idx, 1)        =  1.21836E+02 ;
TOT_FMASS                 (idx, 1)        =  1.21836E+02 ;

% Six-factor formula:

SIX_FF_ETA                (idx, [1:   2]) = [  1.44263E+00 0.00393 ];
SIX_FF_F                  (idx, [1:   2]) = [  2.13452E-02 0.00374 ];
SIX_FF_P                  (idx, [1:   2]) = [  3.72806E-03 0.00047 ];
SIX_FF_EPSILON            (idx, [1:   2]) = [  9.64951E+03 0.00544 ];
SIX_FF_LF                 (idx, [1:   2]) = [  9.69712E-01 8.2E-06 ];
SIX_FF_LT                 (idx, [1:   2]) = [  9.99895E-01 3.0E-07 ];
SIX_FF_KINF               (idx, [1:   2]) = [  1.10648E+00 4.0E-05 ];
SIX_FF_KEFF               (idx, [1:   2]) = [  1.07286E+00 4.4E-05 ];

% Fission neutron and energy production:

NUBAR                     (idx, [1:   2]) = [  2.93059E+00 9.5E-07 ];
FISSE                     (idx, [1:   2]) = [  2.08059E+02 3.3E-08 ];

% Criticality eigenvalues:

ANA_KEFF                  (idx, [1:   6]) = [  1.07285E+00 4.8E-05  1.06936E+00 4.4E-05  3.49334E-03 0.00077 ];
IMP_KEFF                  (idx, [1:   2]) = [  1.07281E+00 2.3E-05 ];
COL_KEFF                  (idx, [1:   2]) = [  1.07282E+00 2.4E-05 ];
ABS_KEFF                  (idx, [1:   2]) = [  1.07281E+00 2.3E-05 ];
ABS_KINF                  (idx, [1:   2]) = [  1.10643E+00 2.0E-05 ];
GEOM_ALBEDO               (idx, [1:   6]) = [  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00 ];

% ALF (Average lethargy of neutrons causing fission):
% Based on E0 = 2.000000E+01 MeV

ANA_ALF                   (idx, [1:   2]) = [  5.01747E+00 2.5E-05 ];
IMP_ALF                   (idx, [1:   2]) = [  5.01754E+00 1.8E-05 ];

% EALF (Energy corresponding to average lethargy of neutrons causing fission):

ANA_EALF                  (idx, [1:   2]) = [  1.32425E-01 0.00012 ];
IMP_EALF                  (idx, [1:   2]) = [  1.32415E-01 9.1E-05 ];

% AFGE (Average energy of neutrons causing fission):

ANA_AFGE                  (idx, [1:   2]) = [  6.98512E-01 9.3E-05 ];
IMP_AFGE                  (idx, [1:   2]) = [  6.98544E-01 4.2E-05 ];

% Forward-weighted delayed neutron parameters:

PRECURSOR_GROUPS          (idx, 1)        = 6 ;
FWD_ANA_BETA_ZERO         (idx, [1:  14]) = [  3.49977E-03 0.00047  8.93031E-05 0.00283  6.76385E-04 0.00109  5.41670E-04 0.00113  1.22865E-03 0.00086  7.11962E-04 0.00114  2.51801E-04 0.00168 ];
FWD_ANA_LAMBDA            (idx, [1:  14]) = [  5.22069E-01 0.00070  1.33827E-02 3.9E-05  3.08068E-02 1.6E-05  1.16998E-01 4.6E-05  3.06742E-01 4.1E-05  8.78105E-01 2.9E-05  2.93747E+00 8.7E-05 ];

% Beta-eff using Meulekamp's method:

ADJ_MEULEKAMP_BETA_EFF    (idx, [1:  14]) = [  3.29065E-03 0.00067  8.29955E-05 0.00431  6.40699E-04 0.00164  5.00619E-04 0.00184  1.16145E-03 0.00105  6.67422E-04 0.00157  2.37459E-04 0.00237 ];
ADJ_MEULEKAMP_LAMBDA      (idx, [1:  14]) = [  5.22667E-01 0.00091  1.33845E-02 5.1E-05  3.08065E-02 2.2E-05  1.17019E-01 7.1E-05  3.06881E-01 4.6E-05  8.78333E-01 4.6E-05  2.93875E+00 0.00013 ];

% Adjoint weighted time constants using Nauchi's method:

IFP_CHAIN_LENGTH          (idx, 1)        = 15 ;
ADJ_NAUCHI_GEN_TIME       (idx, [1:   6]) = [  6.71417E-07 0.00030  6.70762E-07 0.00031  8.72077E-07 0.00474 ];
ADJ_NAUCHI_LIFETIME       (idx, [1:   6]) = [  7.19901E-07 0.00024  7.19199E-07 0.00024  9.35054E-07 0.00475 ];
ADJ_NAUCHI_BETA_EFF       (idx, [1:  14]) = [  3.25651E-03 0.00088  8.12149E-05 0.00509  6.34521E-04 0.00175  4.97345E-04 0.00199  1.14751E-03 0.00153  6.60908E-04 0.00238  2.35019E-04 0.00353 ];
ADJ_NAUCHI_LAMBDA         (idx, [1:  14]) = [  5.22714E-01 0.00127  1.33855E-02 8.5E-05  3.08074E-02 2.9E-05  1.17040E-01 8.4E-05  3.06875E-01 6.9E-05  8.78328E-01 5.8E-05  2.93914E+00 0.00015 ];

% Adjoint weighted time constants using IFP:

ADJ_IFP_GEN_TIME          (idx, [1:   6]) = [  6.32099E-07 0.00090  6.31512E-07 0.00091  8.11546E-07 0.01181 ];
ADJ_IFP_LIFETIME          (idx, [1:   6]) = [  6.77743E-07 0.00084  6.77113E-07 0.00085  8.70161E-07 0.01185 ];
ADJ_IFP_IMP_BETA_EFF      (idx, [1:  14]) = [  3.25973E-03 0.00282  8.10804E-05 0.01743  6.33078E-04 0.00618  4.96517E-04 0.00886  1.15445E-03 0.00478  6.60942E-04 0.00698  2.33656E-04 0.01252 ];
ADJ_IFP_IMP_LAMBDA        (idx, [1:  14]) = [  5.21441E-01 0.00463  1.33876E-02 0.00019  3.08100E-02 0.00011  1.17111E-01 0.00025  3.06878E-01 0.00025  8.78163E-01 0.00022  2.93804E+00 0.00061 ];
ADJ_IFP_ANA_BETA_EFF      (idx, [1:  14]) = [  3.26090E-03 0.00276  8.07270E-05 0.01702  6.32731E-04 0.00603  4.96474E-04 0.00901  1.15511E-03 0.00479  6.61847E-04 0.00666  2.34013E-04 0.01207 ];
ADJ_IFP_ANA_LAMBDA        (idx, [1:  14]) = [  5.21881E-01 0.00443  1.33876E-02 0.00018  3.08100E-02 0.00010  1.17106E-01 0.00024  3.06877E-01 0.00025  8.78165E-01 0.00022  2.93812E+00 0.00059 ];
ADJ_IFP_ROSSI_ALPHA       (idx, [1:   2]) = [ -5.16192E+03 0.00293 ];

% Adjoint weighted time constants using perturbation technique:

ADJ_PERT_GEN_TIME         (idx, [1:   2]) = [  6.53071E-07 0.00042 ];
ADJ_PERT_LIFETIME         (idx, [1:   2]) = [  7.00229E-07 0.00033 ];
ADJ_PERT_BETA_EFF         (idx, [1:   2]) = [  3.26146E-03 0.00149 ];
ADJ_PERT_ROSSI_ALPHA      (idx, [1:   2]) = [ -4.99407E+03 0.00152 ];

% Inverse neutron speed :

ANA_INV_SPD               (idx, [1:   2]) = [  1.45668E-08 0.00011 ];

% Analog slowing-down and thermal neutron lifetime (total/prompt/delayed):

ANA_SLOW_TIME             (idx, [1:   6]) = [  1.62258E-04 0.00013  1.62258E-04 0.00013  1.61994E-04 0.00241 ];
ANA_THERM_TIME            (idx, [1:   6]) = [  7.69230E-05 0.00058  7.69251E-05 0.00058  7.63518E-05 0.00968 ];
ANA_THERM_FRAC            (idx, [1:   6]) = [  4.16214E-03 0.00046  4.16201E-03 0.00046  4.20051E-03 0.00709 ];
ANA_DELAYED_EMTIME        (idx, [1:   2]) = [  1.09012E+01 0.00114 ];
ANA_MEAN_NCOL             (idx, [1:   4]) = [  2.36909E+02 3.4E-05  1.11172E+02 6.1E-05 ];

