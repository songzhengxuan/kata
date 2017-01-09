/*
 * test-driven-detectors4findbugs. Copyright (c) 2011 youDevise, Ltd.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
*/

package com.youdevise.fbplugins.tdd4fb.example;

import static com.youdevise.fbplugins.tdd4fb.DetectorAssert.ofType;

import org.junit.Test;

import tutorial.BigDecBug;
import tutorial.DetectorTutorial;

import com.youdevise.fbplugins.tdd4fb.DetectorAssert;

import edu.umd.cs.findbugs.BugReporter;

public class CustomClassNameLengthDetectorTest {
    @Test public void
    testTutorial() throws Exception {
        BugReporter bugReporter = DetectorAssert.bugReporterForTesting();
        
        DetectorTutorial detector = new DetectorTutorial(bugReporter);
        
        DetectorAssert.assertBugReported(BigDecBug.class, 
                                         detector, bugReporter);
    }

	@Test public void
	raisesAnyBugAgainstClassWithLongName() throws Exception {
		BugReporter bugReporter = DetectorAssert.bugReporterForTesting();
		
		CustomClassNameLengthDetector detector = new CustomClassNameLengthDetector(bugReporter);
		
		DetectorAssert.assertBugReported(ExampleClassWithANameThatIsTooLongForThisSillyDetector.class, 
										 detector, bugReporter);
	}
	
	@Test public void
	raisesABugOfASpecificTypeAgainstClassWithLongName() throws Exception {
		BugReporter bugReporter = DetectorAssert.bugReporterForTesting();
		
		CustomClassNameLengthDetector detector = new CustomClassNameLengthDetector(bugReporter);
		 
		DetectorAssert.assertBugReported(ExampleClassWithANameThatIsTooLongForThisSillyDetector.class, 
				detector, bugReporter, ofType("SILLY_BUG_TYPE"));
	}
	
	@Test public void
	doesNotRaiseABugAgainstClassWhichHasAShortName() throws Exception {
		BugReporter bugReporter = DetectorAssert.bugReporterForTesting();
		CustomClassNameLengthDetector detector = new CustomClassNameLengthDetector(bugReporter);
		
		DetectorAssert.assertNoBugsReported(ExampleClassWithAnAllowedName.class, detector, bugReporter);
	}
	
}
