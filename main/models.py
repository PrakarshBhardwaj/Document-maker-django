from django.db import models
from django.utils.timezone import now as timezone_now
from django.db.models import F
import datetime
import os
#from django.contrib.auth.models import User


class Document(models.Model):
	document_name=models.CharField(max_length=200)
	document_author=models.CharField(max_length=30)
	Creation_date=models.DateField(("Date"),default=datetime.date.today)
	#user=models.ForeignKey(User,on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		is_new = True #if self.Section_id else False
		super(Document, self).save(*args, **kwargs)
		if is_new:
			section = Section(document=self)
			section.Section_Heading = "Default"
			section.save()

	def __str__(self):
		return (self.document_name + "-" + str(self.Creation_date))

class Section(models.Model):
	Section_id=models.AutoField(primary_key=True)
	Section_Heading=models.CharField(max_length=200)
	document=models.ForeignKey(Document,on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		is_new = True if self.Section_id == None else False
		super(Section, self).save(*args, **kwargs)
		if is_new:
			sub_section = Subsection(Section=self)
			sub_section.Subsection_heading = "Default"
			sub_section.save()

class Subsection(models.Model):
	Subsection_id=models.AutoField(primary_key=True)
	Subsection_heading=models.CharField(max_length=200)
	Subsection_sequence = models.CharField(max_length=100, default="")
	Section=models.ForeignKey(Section,on_delete=models.CASCADE)

def add_to_sequence(seq, pos, char):
	cnt = 0
	assert pos > 0, "Position provided is not valid"
	for i,v in enumerate(seq):
		if v == char:
			cnt += 1
		if cnt == pos:
			return seq[:i] + char + seq[i:]
	return seq + char

def delete_from_sequence(seq, pos, char):
	cnt = 0
	assert pos > 0 and pos < len(seq), "Position provided is not valid"
	for i,v in enumerate(seq[:-1]):
		if v == char:
			cnt += 1
		if cnt == pos:
			return seq[:i] + seq[i+1:]
	return seq[:-1]

class Para(models.Model):
	Para_id=models.AutoField(primary_key=True)
	Para_heading=models.CharField(max_length=200)
	Para_content=models.TextField()
	para_number = models.IntegerField(default=0)
	Subsection=models.ForeignKey(Subsection,on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		subsection = Subsection.objects.get(Subsection_id=self.Subsection_id)

		if self._state.adding:
			if self.para_number == 0:      # if para number for new paragraph is not provided for new para
				last_para_number = Para.objects.filter(Subsection=self.Subsection).aggregate(largest=models.Max('para_number'))['largest']

				if last_para_number is not None:
					self.para_number = last_para_number + 1
				else:
					self.para_number = 1
			else:
				para_set = Para.objects.filter(Subsection=self.Subsection, para_number__gte=self.para_number).update(para_number=F('para_number')+1)

			subsection.Subsection_sequence = add_to_sequence(subsection.Subsection_sequence, self.para_number, "P")
			super(Para, self).save(*args, **kwargs)

		elif self._state.db:
			prev_instance = Para.objects.get(Para_id=self.Para_id)
			# prev_last = Para.objects.filter(Subsection=self.Subsection).aggregate(largest=models.Max('para_number'))['largest']
			super(Para, self).save(*args, **kwargs)
			temp_seq = delete_from_sequence(subsection.Subsection_sequence, prev_instance.para_number, "P")

			if prev_instance.para_number > self.para_number:
				para_set = Para.objects.filter(Subsection=self.Subsection, para_number__gte=self.para_number).exclude(Para_id=self.Para_id).update(para_number=F('para_number')+1)

			if prev_instance.para_number < self.para_number:
				para_set = Para.objects.filter(Subsection=self.Subsection, para_number__lte=self.para_number).exclude(Para_id=self.Para_id).update(para_number=F('para_number')-1)
			
			subsection.Subsection_sequence = add_to_sequence(temp_seq, self.para_number, "P")
		
		subsection.save()
	
	def delete(self, *args, **kwargs):
		subsection = Subsection.objects.get(Subsection_id=self.Subsection_id)
		subsection.Subsection_sequence = delete_from_sequence(subsection.Subsection_sequence, self.para_number, "P")
		subsection.save()
		para_set = Para.objects.filter(Subsection=self.Subsection, para_number__gte=self.para_number).exclude(Para_id=self.Para_id).update(para_number=F('para_number')-1)
		super(Para, self).delete()


def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return f"imgs/{now:%Y/%m/%Y%m%d%H%M%S}{ext}"

class Img(models.Model):
	Img_id=models.AutoField(primary_key=True)
	Img_heading=models.CharField(max_length=100)
	Img_Data = models.ImageField(upload_to="imgs/", blank=True, null=True)
	Img_url=models.URLField(max_length = 200,default='https://www.google.com/')
	img_number = models.IntegerField(default=0)
	Subsection=models.ForeignKey(Subsection,on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		subsection = Subsection.objects.get(Subsection_id=self.Subsection_id)

		if self._state.adding:
			if self.img_number == 0:      # if para number for new paragraph is not provided for new para
				last_img_number = Img.objects.filter(Subsection=self.Subsection).aggregate(largest=models.Max('img_number'))['largest']

				if last_img_number is not None:
					self.img_number = last_img_number + 1
				else:
					self.img_number = 1
			else:
				raise Exception("Img number cannot be expilicity provided.")
			
			print(self.img_number)
			subsection.Subsection_sequence = add_to_sequence(subsection.Subsection_sequence, self.img_number, "I")
			super(Img, self).save(*args, **kwargs)

		elif self._state.db:
			prev_instance = Img.objects.get(Img_id=self.Img_id)
			assert self.img_number == prev_instance.img_number, "Image number cannot be changed."
			super(Img, self).save(*args, **kwargs)

		subsection.save()

	def delete(self, *args, **kwargs):
		subsection = Subsection.objects.get(Subsection_id=self.Subsection_id)
		subsection.Subsection_sequence = delete_from_sequence(subsection.Subsection_sequence, self.img_number, "I")
		subsection.save()
		img_set = Img.objects.filter(Subsection=self.Subsection, img_number__gte=self.img_number).exclude(Img_id=self.Img_id).update(img_number=F('img_number')-1)
		super(Img, self).delete()