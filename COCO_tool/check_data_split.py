from pycocotools.coco import COCO

train = '../annotations/instances_train2017.json'
val = '../annotations/instances_val2017.json'
test = '../annotations/image_info_test2017.json'

coco_train = COCO(train)
train_ids = coco_train.getImgIds()
train_set = set(train_ids)

coco_val = COCO(val)
val_ids = coco_val.getImgIds()
val_set = set(val_ids)

coco_test = COCO(test)
test_ids = coco_test.getImgIds()
test_set = set(test_ids)

print()
print('len of train:', len(train_ids))
print('len of val:', len(val_ids))
print('len of test:', len(test_ids))
print()
print('intersect of train and val:', len(train_set.intersection(val_set)))
print('intersect of val and test:', len(test_set.intersection(val_set)))
print('intersect of train and test:', len(train_set.intersection(test_set)))