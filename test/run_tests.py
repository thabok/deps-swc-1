import os
import sys

from btc_embedded import EPRestApi, util


def run_btc_test(epp_path, work_dir=os.getcwd()):
    epp_path = os.path.abspath(epp_path)
    work_dir = os.path.dirname(epp_path)
    
    # BTC EmbeddedPlatform API object
    ep = EPRestApi()

    # Load a BTC EmbeddedPlatform profile (*.epp)
    ep.get(f'profiles/{epp_path}?discardCurrentProfile=true', message="Loading profile")

    # Update architecture (incl. code generation)
    ep.put('architectures', message="Updating Architecture")

    # Execute requirements-based tests
    scopes = ep.get('scopes')
    scope_uids = [scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink']
    toplevel_scope_uid = scope_uids[0]
    rbt_exec_payload = {
        'UIDs': scope_uids,
        'data' : {
            'execConfigNames' : [ 'SL MIL', 'SIL' ]
        }
    }
    response = ep.post('scopes/test-execution-rbt', rbt_exec_payload, message="Executing requirements-based tests")
    rbt_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-rbt?goal-types=MCDC")
    util.print_rbt_results(response, rbt_coverage)

    # automatic test generation
    vector_gen_config = { 'pllString' : 'MCDC;CA;DZ', 'scopeUid' : toplevel_scope_uid }
    ep.post('coverage-generation', vector_gen_config, message="Generating vectors")
    b2b_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-b2b?goal-types=MCDC")

    # B2B TL MIL vs. SIL
    response = ep.post(f"scopes/{toplevel_scope_uid}/b2b", { 'refMode': 'SL MIL', 'compMode': 'SIL' }, message="Executing B2B test")
    util.print_b2b_results(response, b2b_coverage)

    # Create project report
    report = ep.post(f"scopes/{toplevel_scope_uid}/project-report?template-name=rbt-b2b", message="Creating test report")
    # export project report to a file called 'report.html'
    ep.post(f"reports/{report['uid']}", { 'exportPath': work_dir, 'newName': 'test_report' })

    # Save *.epp
    ep.put('profiles', { 'path': epp_path }, message="Saving profile")

    print('Finished btc test workflow.')


# if the script is called directly: expect
# - the first argument to be the epp path
if __name__ == '__main__':
    run_btc_test(sys.argv[1])
    # run_btc_test('test/shared_module_a.epp')
    