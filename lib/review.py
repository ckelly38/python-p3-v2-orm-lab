from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.setYear(year);
        self.setSummary(summary);
        self.setEmployeeId(employee_id);

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        CURSOR.execute("INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?)",
                             (self.year, self.summary, self.employee_id));
        self.id = CURSOR.lastrowid;

    def getYear(self):
        return self._year;

    def setYear(self, val):
        if (type(val) == int and (val > 2000 or val == 2000)): self._year = val;
        else: raise ValueError("year must be a number greater than or equal to 2000!");

    year = property(getYear, setYear);

    def getSummary(self):
        return self._summary;

    def setSummary(self, val):
        if (type(val) == str and (len(val) > 0)): self._summary = val;
        else: raise ValueError("summary must be a non-empty string!");

    summary = property(getSummary, setSummary);

    def getEmployeeId(self):
        return self._employee_id;

    def setEmployeeId(self, val):
        if type(val) is int and Employee.find_by_id(val): self._employee_id = val;
        else: raise ValueError("employee_id must reference a department in the database");

    employee_id = property(getEmployeeId, setEmployeeId);

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        rev = cls(year, summary, employee_id);
        rev.save();
        cls.all.update({rev.id: rev});
        return rev;
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for existing instance using the row's primary key
        #print(row);
        revs = cls.all;
        for key in revs:
            rev = revs[key];
            #print(rev);
            if (rev.year == row[1] and rev.summary == row[2] and rev.employee_id == row[3]): return rev;
        #print("row is not saved! Perhaps it is in the database!");
        ores = CURSOR.execute("SELECT * FROM reviews WHERE year = ?", (row[1],));
        #print(f"CURSOR.lastrowid = {CURSOR.lastrowid}");
        if (ores == None): pass;
        else: return cls(row[1], row[2], row[3], CURSOR.lastrowid);
        return None;
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        #review = CURSOR.execute("SELECT * FROM reviews WHERE id = ?", (id,));
        #CONN.commit();
        #return review;
        print(id);
        revs = cls.all;
        for key in revs:
            rev = revs[key];
            print(rev);
            if (rev.id == id): return rev;
        return None;

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        pass

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        pass

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        return cls.all;

