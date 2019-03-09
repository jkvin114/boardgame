#-*- coding: ms949 -*-
items=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
class Item():
    def __init__(self,id,name,price,ability,level):
        self.id=id
        self.name=name
        self.price=price
        self.ability=ability
        self.parent=None
        self.child1=None
        self.child2=None
        self.level=level
        
        
        #  self.skillability=[self.MaxHP,self.AD,self.AP,self.AR,self.MR,self.arP,self.MP,self.absorb,self.regen,
        #                               0          1            2         3        4        5        6           7            8             
        # 9. adStat 10.basicattackrange   11.addMdmg  12. skilldmgReduction

               
class abil():
    def __init__(self,id,amount):
        self.id=id
        self.value=amount
        
        
Sword1=Item(0,"1��� ��",300,[abil(1,80),abil(5,20)],3)
Sword2=Item(1,"2��� ��",80,[abil(1,30)],2)
Sword3=Item(2,"3��� ��",30,[abil(1,10)],1)
Sword1.child1=Sword2
Sword1.child2=Sword2
Sword2.child1=Sword3
Sword2.child2=Sword3
Sword2.parent=Sword1
Sword3.parent=Sword2

Marble1=Item(3,"1��� ����",320,[abil(2,120)],3)
Marble2=Item(4,"2��� ����",120,[abil(2,50)],2)
Marble3=Item(5,"3��� ����",40,[abil(2,20)],1)
Marble1.child1=Marble2
Marble1.child2=Marble2
Marble2.child1=Marble3
Marble2.child2=Marble3
Marble2.parent=Marble1
Marble3.parent=Marble2

Shield1=Item(6,"1��� ����",300,[abil(3,80),abil(0,100)],3)
Shield2=Item(7,"2��� ����",80,[abil(3,30),abil(0,30)],2)
Shield3=Item(8,"3��� ����",30,[abil(3,10),abil(0,10)],1)
Shield1.child1=Shield2
Shield1.child2=Shield2
Shield2.child1=Shield3
Shield2.child2=Shield3
Shield2.parent=Shield1
Shield3.parent=Shield2

Fruit1=Item(9,"1��� ����",400,[abil(0,100),abil(8,30)],3)
Fruit2=Item(10,"2��� ����",120,[abil(0,60),abil(8,10)],2)
Fruit3=Item(11,"3��� ����",40,[abil(8,5)],1)
Fruit1.child1=Fruit2
Fruit1.child2=Fruit2
Fruit2.child1=Fruit3
Fruit2.child2=Fruit3
Fruit2.parent=Fruit1
Fruit3.parent=Fruit2

Armor1=Item(12,"1��� ����",300,[abil(4,100),abil(0,120)],3)
Armor2=Item(13,"2��� ����",100,[abil(4,40),abil(0,30)],2)
Armor3=Item(14,"3��� ����",40,[abil(4,10),abil(0,10)],1)
Armor1.child1=Armor2
Armor1.child2=Armor2
Armor2.child1=Armor3
Armor2.child2=Armor3
Armor2.parent=Armor1
Armor3.parent=Armor2

GuardianAngel=Item(15,"��ȣõ��",350,[abil(4,70),abil(3,50),abil(0,60)],3)
AbsorbSword=Item(16,"�����ǰ�",40,[abil(7,10)],2)
BloodSword=Item(17,"�Ǻ񸰰�",250,[abil(7,30),abil(1,30)],3)
GuardianAngel.child1=Armor2
GuardianAngel.child2=Shield2
BloodSword.child1=AbsorbSword
BloodSword.child2=Sword2

NaturePower1=Item(18,"���ڿ�����",300,[abil(12,40),abil(0,40)],3)
NaturePower2=Item(19,"�ڿ�����",70,[abil(12,10)],2)
NaturePower3=Item(20,"��������",40,[abil(12,5)],1)
Ruby=Item(21,"��� ����",35,[abil(0,40)],2)
AncientSpear=Item(22,"����� â",300,[abil(9,30),abil(11,25)],3)
KillerWhip=Item(23,"������ ä��",340,[abil(9,80),abil(10,2)],3)
CunningWhip=Item(24,"��Ȱ�� ä��",45,[abil(10,1)],2)
MagicWeapon2=Item(25,"�߱� �����ǹ���",135,[abil(9,50)],2)
MagicWeapon3=Item(26,"�ʱ� �����ǹ���",35,[abil(9,10)],1)
BloodOrb=Item(27,"���� ����",60,[abil(11,5)],1)



MagicWeapon2.child1=MagicWeapon3
MagicWeapon2.child2=MagicWeapon3

KillerWhip.child1=MagicWeapon2
KillerWhip.child2=CunningWhip

AncientSpear.child1=MagicWeapon2
AncientSpear.child2=BloodOrb

NaturePower2.child1=NaturePower3
NaturePower2.child2=NaturePower3

NaturePower1.child1=NaturePower2
NaturePower1.child2=Ruby


allItem=[Sword1,Sword2,Sword3,Marble1,Marble2,Marble3,Shield1,Shield2,Shield3,Fruit1,Fruit2,Fruit3,
         Armor1,Armor2,Armor3,GuardianAngel,AbsorbSword,BloodSword,NaturePower1,NaturePower2,NaturePower3,
         Ruby,AncientSpear,KillerWhip,CunningWhip,MagicWeapon2,MagicWeapon3,BloodOrb]



