def config_parser():

    import configargparse
    parser = configargparse.ArgumentParser()
    parser.add_argument('--config', is_config_file=True, default='./configs/DTU2.txt',
                        help='config file path')
    parser.add_argument("--expname", type=str,
                        help='experiment name')
    parser.add_argument("--basedir", type=str, default='./logs/',
                        help='where to store ckpts and logs')
    parser.add_argument("--datadir", type=str, default='./data/nerf_synthetic/lego',
                        help='input data directory')
    parser.add_argument("--datadir_test", type=str, default='./data/nerf_synthetic/lego',
                        help='input data directory for test images')

    # training options
    parser.add_argument("--fine_tune", type=str, default='None',
                        help='scan to fine tune to')
    parser.add_argument("--lrate_decay_off", type=bool, default=False,
                        help='turn off lrate decay')
    parser.add_argument("--split", type=str, default='split.pkl',
                        help='name of split file')
    parser.add_argument("--model", type=str, default='model1',
                        help='the neural model to use')
    parser.add_argument("--fine_model_duplicate", type=bool, default=True,
                        help='if true use the same model for fine and coarse hierarchical sampling')
    parser.add_argument("--netdepth", type=int, default=8,
                        help='layers in network')
    parser.add_argument("--netwidth", type=int, default=256,
                        help='channels per layer')
    parser.add_argument("--netdepth_fine", type=int, default=8,
                        help='layers in fine network')
    parser.add_argument("--netwidth_fine", type=int, default=256,
                        help='channels per layer in fine network')
    parser.add_argument("--N_rand", type=int, default=32*32*4,
                        help='batch size (number of random rays per gradient step)')
    parser.add_argument("--lrate", type=float, default=5e-4,
                        help='learning rate')
    parser.add_argument("--lrate_decay", type=int, default=250,
                        help='exponential learning rate decay (in 1000 steps)')
    parser.add_argument("--chunk", type=int, default=1024*32,
                        help='number of rays processed in parallel, decrease if running out of memory')
    parser.add_argument("--netchunk", type=int, default=1024*64,
                        help='number of pts sent through network in parallel, decrease if running out of memory')
    parser.add_argument("--no_batching", action='store_true',
                        help='only take random rays from 1 image at a time')
    parser.add_argument("--no_reload", action='store_true',
                        help='do not reload weights from saved ckpt')
    parser.add_argument("--ft_path", type=str, default=None,
                        help='Specific NN parameter file (npy) to reload for the network.'
                             'Given string is appended to the experiments folder path.')
    parser.add_argument("--batch_size", type=int, default=1,
                        help='number of training images used per batch')
    parser.add_argument("--precrop_iters", type=int, default=0,
                        help='number of steps to train on central crops')
    parser.add_argument("--precrop_frac", type=float,
                        default=.5, help='fraction of img taken for central crops')
    parser.add_argument("--sigmoid", type=bool, default=False,
                        help='if true, use sigmoid to activate raw predicion with sigmoid, relu else')
    # learning setup
    parser.add_argument("--num_reference_views", type=int, default=10,
                        help='number of reference views given to the network as input to predict a novel view')

    # rendering options
    parser.add_argument('--video', dest='video', action='store_true')
    parser.set_defaults(video=False)

    parser.add_argument("--N_rays_test", type=int, default=128,
                        help='number of rays considered par batch in test mode')
    parser.add_argument("--N_samples", type=int, default=64,
                        help='number of coarse samples per ray')
    parser.add_argument("--N_importance", type=int, default=0,
                        help='number of additional fine samples per ray')
    parser.add_argument("--perturb", type=float, default=1.,
                        help='set to 0. for no jitter, 1. for jitter')
    parser.add_argument("--use_viewdirs", action='store_true',
                        help='use full 5D input instead of 3D')
    parser.add_argument("--i_embed", type=int, default=0,
                        help='set 0 for default positional encoding, -1 for none')
    parser.add_argument("--multires", type=int, default=10,
                        help='log2 of max freq for positional encoding (3D location)')
    parser.add_argument("--multires_views", type=int, default=4,
                        help='log2 of max freq for positional encoding (2D direction)')
    parser.add_argument("--raw_noise_std", type=float, default=0.,
                        help='std dev of noise added to regularize sigma_a output, 1e0 recommended')

    parser.add_argument("--render_only", action='store_true',
                        help='do not optimize, reload weights and render out render_poses path')
    parser.add_argument("--render_test", action='store_true',
                        help='render the test set instead of render_poses path')
    parser.add_argument("--render_factor", type=int, default=4,
                        help='Downsampling factor to speed up test time rendering of images. 1 is full size, set to 4 or 8 for faster preview.')

    # dataset options
    parser.add_argument("--dataset_type", type=str, default='DTU',
                        help='options: llff / blender / deepvoxels / DTU')
    parser.add_argument("--testskip", type=int, default=8,
                        help='will load 1/N images from test/val sets, useful for large datasets like deepvoxels')


    parser.add_argument("--generate_specific_samples", action='append', type=str, default=None,
                        help='visualize specific samples in generation')
    parser.add_argument("--near", type=int, default=None,
                        help='near clipping plane location')
    parser.add_argument("--far", type=int, default=None,
                        help='far clipping plane location')

    ## generation options
    parser.add_argument("--eval", type=bool, default=False,
                        help='turn on eval mode - render images from eval poses')
    parser.add_argument("--gen_pose", type=int, default=None,
                        help='what pose to generate for video or evaluation')
    parser.add_argument("--fixed_batch", type=int, default=0,
                        help='A fixed batch of input reference images is loaded. Inputs are divided into batches'
                             'of size num_reference_views keeping their ordering in the split file.')


    ## deepvoxels flags
    parser.add_argument("--shape", type=str, default='greek',
                        help='options : armchair / cube / greek / vase')

    ## blender flags
    parser.add_argument("--white_bkgd", action='store_true',
                        help='set to render synthetic data on a white bkgd (always use for dvoxels)')
    parser.add_argument("--half_res", action='store_true',
                        help='load blender synthetic data at 400x400 instead of 800x800')

    ## llff flags
    parser.add_argument("--factor", type=int, default=8,
                        help='downsample factor for LLFF images')
    parser.add_argument("--dtu_size", action='store_true',
                        help='set, in order to use 1200x1600 HxW for llff data')
    parser.add_argument("--no_ndc", action='store_true',
                        help='use normalized device coordinates (set for non-forward facing scenes)')
    # this is set false in all cases in the paper
    parser.add_argument("--lindisp", action='store_true',
                         help='sampling linearly in disparity rather than depth')
    parser.add_argument("--spherify", action='store_true',
                        help='set for spherical 360 scenes')
    parser.add_argument("--llffhold", type=int, default=8,
                        help='will take every 1/N images as LLFF test set, paper uses 8')

    # logging/saving options
    parser.add_argument("--i_print",   type=int, default=100,
                        help='frequency of console printout and metric loggin')
    parser.add_argument("--i_val_fine_tune",   type=int, default=200,
                        help='frequency of val loss computation in fine tuning mode')
    parser.add_argument("--i_img",     type=int, default=500,
                        help='frequency of tensorboard image logging')
    parser.add_argument("--i_weights", type=int, default=1000,
                        help='frequency of weight ckpt saving')
    parser.add_argument("--i_no_val", action='store_true',
                        help='turn off validation computation')
    parser.add_argument("--i_testset", type=int, default=1000,
                        help='frequency of testset saving')
    parser.add_argument("--i_video",   type=int, default=50000,
                        help='frequency of render_poses video saving')
    parser.add_argument("--i_validation_loss",   type=int, default=500,
                        help='frequency of val loss computation')

    return parser


def get_config():

    parser = config_parser()
    cfg = parser.parse_args()
    return cfg