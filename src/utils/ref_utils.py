import re

titles = ['Mr.', 'Mr', 'Mrs.', 'Mrs', 'Miss', 'Dr.', 'Dr', 'Sir', 'Ms.', 'Ms']


def create_name_ref(x):
    ref = x.split()
    ref = [t for t in ref if t not in titles]
    ref.insert(0, ref.pop(-1))
    ref = '#{}'.format('_'.join(ref))
    return re.sub(r'\.|,', '', ref)


def create_initials_ref(x):
    ref = x.split()
    ref = [t for t in ref if t not in titles]
    ref = re.sub('[^A-Z]', '', ''.join(ref))
    return ref


def create_ref(x):
    ref = x.split()
    ref = '#{}'.format('_'.join(ref))
    return re.sub(r'\.|,', '', ref)


