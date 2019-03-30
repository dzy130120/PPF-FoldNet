from dataset import ShapeNetDataset
from matplotlib import pyplot as plt
from visualize import draw_pts
from model import FoldNet


def show_reconstructed(model, class_choice='Airplane'):
    dataroot = "data/shapenetcore_partanno_segmentation_benchmark_v0"
    dataset = ShapeNetDataset(root=dataroot,
                              class_choice=class_choice,
                              split='train',
                              classification=True,
                              num_points=2048,
                              )
    pts, _ = dataset[0]
    reconstructed_pl = model(pts.view(1, 2048, 3))[0]
    ax1, _ = draw_pts(pts, clr=None, cmap='CMRmap')
    ax2, _ = draw_pts(reconstructed_pl.detach().numpy(), clr=None, cmap='CMRmap')
    ax1.figure.show()
    ax2.figure.show()
    # fig = plt.figure()
    # ax1 = plt.subplot(121)
    # ax2 = plt.subplot(122)
    # draw_pts(pts, clr=None, cmap='CMRmap', ax=ax1)
    # draw_pts(reconstructed_pl.detach().numpy(), clr=None, cmap='CMRmap', ax=ax2)
    # fig.add_subplot(ax1)
    # fig.add_subplot(ax2)
    # plt.show()


def interpolate(model, class1='Airplane', class2=None):
    dataroot = "data/shapenetcore_partanno_segmentation_benchmark_v0"
    dataset1 = ShapeNetDataset(root=dataroot,
                               class_choice=class1,
                               split='train',
                               classification=True,
                               num_points=2048,
                               )
    pts1, _ = dataset1[0]
    codeword1 = model.encoder(pts1.view(1, 2048, 3))
    # intra-class or inter-class
    if class2 is None:
        dataset2 = ShapeNetDataset(root=dataroot,
                                   class_choice=class2,
                                   split='train',
                                   classification=True,
                                   num_points=2048)
        pts2, _ = dataset2[0]
        codeword2 = model.encoder(pts2.view(1, 2048, 3))
    else:
        pts2, _ = dataset1[0]
        codeword2 = model.encoder(pts2.view(1, 2048, 3))

    # do interpolation.
    # ratio = [0, 0.2, 0.4, 0.6, 0.8, 1]
    ratio = [0, 1]
    for u in range(len(ratio)):
        mix_codeword1 = (1 - ratio[u]) * codeword1 + ratio[u] * codeword2
        output = model.decoder(mix_codeword1)
        plt.subplot(1, u + 1, 1)
        pts = output[0].detach().numpy()
        ax, _ = draw_pts(pts, clr=None, cmap='CMRmap')
        ax.figure.show()


if __name__ == '__main__':
    pretrain = 'models/shapenet_best.pth'
    model = FoldNet(num_points=2048)
    model.load_state_dict(model.state_dict(), pretrain)
    show_reconstructed(model, 'Chair')
    # interpolate(model, "Airplane", "Table")
