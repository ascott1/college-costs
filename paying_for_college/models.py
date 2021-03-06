from django.db import models
import uuid


class ConstantRate(models.Model):
    """Rate values that generally only change annually"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,
                            blank=True,
                            help_text="VARIABLE NAME FOR JS")
    value = models.DecimalField(max_digits=6, decimal_places=5)
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"%s (%s), updated %s" % (self.name, self.slug, self.updated)

    class Meta:
        ordering = ['slug']


class ConstantCap(models.Model):
    """Cap values that generally only change annually"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,
                            blank=True,
                            help_text="VARIABLE NAME FOR JS")
    value = models.IntegerField()
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"%s (%s), updated %s" % (self.name, self.slug, self.updated)

    class Meta:
        ordering = ['name']


class School(models.Model):
    """
    Represents a school
    """
    school_id = models.IntegerField(primary_key=True)
    data_json = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    accreditor = models.CharField(max_length=255, blank=True)
    url = models.TextField(blank=True)
    degrees_predominant = models.TextField(blank=True)
    degrees_highest = models.TextField(blank=True)
    operating = models.BooleanField(default=True)
    KBYOSS = models.BooleanField(default=False)  # shopping-sheet participant

    def __unicode__(self):
        return self.primary_alias + u" (%s)" % self.school_id

    @property
    def primary_alias(self):
        if len(self.alias_set.values()) != 0:
            return self.alias_set.get(is_primary=True).alias
        else:
            return 'Not Available'


class Contact(models.Model):
    """school email account to which we send confirmations"""
    institution = models.ForeignKey(School)
    contact = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.contact + u" (%s)" % unicode(self.institution)


class Program(models.Model):
    """
    Cost and outcome info for an individual course of study at a school
    """
    institution = models.ForeignKey(School)
    program_name = models.CharField(max_length=255)
    level = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=255, blank=True)
    total_cost = models.IntegerField(blank=True, null=True)
    time_to_complete = models.IntegerField(blank=True,
                                           null=True,
                                           help_text="IN DAYS")
    completion_rate = models.DecimalField(blank=True,
                                          null=True,
                                          max_digits=5,
                                          decimal_places=2)
    default_rate = models.DecimalField(blank=True,
                                       null=True,
                                       max_digits=5,
                                       decimal_places=2)
    job_rate = models.DecimalField(blank=True,
                                   null=True,
                                   max_digits=5,
                                   decimal_places=2,
                                   help_text="COMPLETERS WHO GET RELATED JOB")
    salary = models.IntegerField(blank=True, null=True)
    program_length = models.IntegerField(blank=True,
                                         null=True,
                                         help_text="IN DAYS")
    program_cost = models.IntegerField(blank=True,
                                       null=True,
                                       help_text="TUITION & FEES")
    housing = models.IntegerField(blank=True,
                                  null=True,
                                  help_text="HOUSING & MEALS")
    books = models.IntegerField(blank=True,
                                null=True,
                                help_text="BOOKS & SUPPLIES")
    transportation = models.IntegerField(blank=True, null=True)
    other_costs = models.IntegerField(blank=True,
                                      null=True,
                                      help_text="BOOKS & SUPPLIES")

    def __unicode__(self):
        return u"%s (%s)" % (self.program_name, unicode(self.institution))

# class Offer(models.Model):
#     """
#     Financial aid package offered to a prospective student
#     """
#     school = models.ForeignKey(School)
#     program = models.ForeignKey(Program)
#     student_id = models.CharField(max_length=255)
#     uuid = models.CharField(max_length=100, blank=True)
#     # COST OF ATTENDANCE
#     tuition = models.PositiveIntegerField(default=0,
#                                           help_text="TUITION & FEES")  # tui
#     housing = models.PositiveIntegerField(default=0,
#                                           help_text="HOUSING & MEALS")  # hou
#     books = models.PositiveIntegerField(default=0,
#                                         help_text="BOOKS & SUPPLIES")  # bks
#     other = models.PositiveIntegerField(default=0,
#                                         help_text="OTHER EXPENSES")  # oth
#     # MONEY FOR SCHOOL
#     scholarships = models.IntegerField(default=0,
#                                        help_text="SCHOLARSHIPS & GRANTS")
#     pell_grant = models.PositiveIntegerField(default=0)
#     tuition_assist = models.PositiveIntegerField(default=0,
#                                                  help_text='SCHOLARSHIPS')
#     mil_assist = models.PositiveIntegerField(default=0,
#                                              help_text='MILITARY ASSISTANCE')
#     gi_bill = models.PositiveIntegerField(default=0)
#     you_pay = models.PositiveIntegerField(default=0)
#     family_pay = models.PositiveIntegerField(default=0)
#     work_study = models.PositiveIntegerField(default=0)
#     parent_loans = models.PositiveIntegerField(default=0)
#     perkins_loans = models.PositiveIntegerField(default=0)
#     subsidized_loans = models.PositiveIntegerField(default=0)
#     unsubsidized_loans = models.PositiveIntegerField(default=0)
#     plus_loans = models.PositiveIntegerField(default=0)
#     private_loans = models.PositiveIntegerField(default=0)
#     private_loan_interest = models.DecimalField(default=0.0,
#                                                 max_digits=5,
#                                                 decimal_places=2)
#     school_loans = models.PositiveIntegerField(default=0)
#     school_loan_interest = models.DecimalField(default=0.0,
#                                                max_digits=5,
#                                                decimal_places=2)
#     timestamp = models.DateTimeField(blank=True, null=True)
#     in_state = models.NullBooleanField(help_text="ONLY FOR PUBLIC SCHOOLS")

#     def save(self, *args, **kwargs):
#         if not self.uuid:
#             self.uuid = str(uuid.uuid4())
#         super(Offer, self).save(*args, **kwargs)


class Alias(models.Model):
    """
    One of potentially several names for a school
    """
    institution = models.ForeignKey(School)
    alias = models.TextField()
    is_primary = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s (alias for %s)" % (self.alias, unicode(self.institution))

    class Meta:
        verbose_name_plural = "Aliases"


class Nickname(models.Model):
    """
    One of potentially several nicknames for a school
    """
    institution = models.ForeignKey(School)
    nickname = models.TextField()
    is_female = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s (nickname for %s)" % (self.nickname,
                                          unicode(self.institution))

    class Meta:
        ordering = ['nickname']


class BAHRate(models.Model):
    """
    Basic Allowance for Housing (BAH) rates are zipcode-specific.
    Used in GI Bill data and may go away.
    """
    zip5 = models.CharField(max_length=5)
    value = models.IntegerField()


class Worksheet(models.Model):
    """
    The saved state of a student's comaprison worksheet.
    This is likely to go away.
    """
    guid = models.CharField(max_length=64, primary_key=True)
    saved_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Feedback(models.Model):
    """
    User-submitted feedback
    """
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


def print_vals(obj, val_list=False, val_dict=False):
    """inspect a Django db object"""
    keylist = sorted([key for key in obj._meta.get_all_field_names()],
                     key=lambda s: s.lower())
    try:
        print "%s values for %s:\n" % (obj._meta.object_name, obj)
    except:  # pragma: no cover
        pass
    if val_list:
        for key in keylist:
            try:
                obj.__getattribute__(key)
            except:
                del keylist[keylist.index(key)]
        return [obj.__getattribute__(key) for key in keylist]
    elif val_dict:
        return obj.__dict__
    else:
        for key in keylist:
            try:
                print "%s: %s" % (key, obj.__getattribute__(key))
            except:  # pragma: no cover
                pass
