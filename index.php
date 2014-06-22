<HTML>
<HEAD>
<TITLE>Extra Stats from Logs.tf & SupStats2</TITLE>

<link rel="stylesheet" href="bootstrap.css">
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="dashboard.css">
</HEAD>

<BODY>
	<div class="navbar navbar-default navbar-fixed-top" role="navigation">
		<div class="container-fluid">
			<div class="navbar-header">
				<a class="navbar-brand" href="/tfstats">Sample Logs for Extra Stats (Logs.tf & SupStats2)</a>
			</div>
		</div>
	</div>
<? 
	$dir = 'logs/';
	$logs = scandir($dir);
	?>
	<div class="container-fluid">
		<div class="row">
			<div class="col-sm-3 col-md-2 sidebar">
				<ul class="nav nav-sidebar">
					<li><a href="#"><u>W/O Class Data</u></a></li>
	<?
	foreach ($logs as $l):
		if($l != "." && $l != ".."):
	?>
			<li class="<? echo (isset($_GET['log']) && isset($_GET['classes']) && $_GET['log']==substr($l,0,-4)) ? 'active' : ''; ?>"><a href="?log=<? echo substr($l,0,-4); ?>&classes=false"><? echo substr($l,0,-4); ?></a></li>
	<?
		endif;
	endforeach;
	?>
				</ul>
				<ul class="nav nav-sidebar">
					<li><a href="#"><u>W/ Class Data</u></a></li>

	<?
	foreach ($logs as $l):
		if($l != "." && $l != ".."):
	?>
			<li class="<? echo (isset($_GET['log']) && !isset($_GET['classes']) && $_GET['log']==substr($l,0,-4)) ? 'active' : ''; ?>"><a href="?log=<? echo substr($l,0,-4); ?>"><? echo substr($l,0,-4); ?></a></li>
	<?
		endif;
	endforeach;
	?>
				</ul>
				<ul class="nav nav-sidebar">
					<li><a href="https://github.com/mnemyx/logstfextra"><u>Github</u></a></li>
				</ul>
			</div>

			<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<?

	if (isset($_GET["log"]) && !empty($_GET["log"])):

		$logloc = "logs/" . $_GET["log"] . ".log";

		if (file_exists($logloc)):
			$classes = (isset($_GET["classes"]) && $_GET["classes"] == "false") ? 0 : 1;
			$execstr = (isset($_GET["classes"]) && $_GET["classes"] == "false") ? '/usr/bin/python noclasses_extrastats.py ' . $logloc : '/usr/bin/python extrastats.py ' . $logloc;

			// var_dump(utf8_encode(shell_exec($execstr)), true);
			$data = json_decode(shell_exec($execstr), true);
			//var_dump($data);

			if (!empty($data)):

				foreach ($data as $key => $val):
					// key 0 = damaged given, key 1 = damaged received 
					$type = (!$key) ? "Damaged Given" : "Damage Received"; ?>
					<div style="width: 45%; float: left; padding: 0px 20px;">
					<h2 class="sub-header"><? echo $type; ?></h2>

					<? // sort by player's team + damage
					$psortda = array();
					$psortteam = array();
					foreach ($val[1] as $player => $stats) {
						$psortda[$player] = $stats['total_da'];
						$psortteam[$player] = $stats['pdata']['team'];
					} 

					if (!$key)
						array_multisort($psortda, SORT_DESC, $val[1]);
					else
						array_multisort($psortda, SORT_ASC, $val[1]);

					// printing data
					foreach ($val[1] as $player => $stats): ?>
					
					<div class="panel panel-<? echo ($stats['pdata']['team'] == "Blue") ? 'info' : 'danger'; ?>">
					<div class="panel-heading"><? echo $stats['pdata']['pname']; ?></div>
					<div class="panel-body">
					<table class="table <? echo (!$classes) ? "table-striped" : ""; ?>">
						<thead>
						<tr>
							<th><? echo 'Total '.$type; ?></th>
							<th class="right"><? echo $stats['total_da']; ?></th>
						</tr>
						</thead>
						<tbody>
						<? if (!$classes):
							// sorting by damage numbers desc
							$daNums = array();
							foreach($stats['players'] as $pname => $pstats)
								$daNums[$pname] = $pstats['da'];
							array_multisort($daNums, SORT_DESC, $stats['players']);

							// printing data
							foreach ($stats['players'] as $pname => $pstats): ?>
								<tr>
									<td><? echo $pstats['pdata']['pname']; ?></td>
									<td align="right"><? echo $pstats['da']; ?></td>
								</tr>	
						<?	endforeach; 
						else: // sort by the total damage per main player's class
							$pcsortda = array();
							foreach($stats['classes'] as $class => $cstats)
								$pcsortda[$class] = $cstats['total_da'];
							array_multisort($pcsortda, SORT_DESC, $stats['classes']);

							// printing data
							foreach ($stats['classes'] as $class => $cstats): ?>
								<tr class="mp-class">
									<td>playing as <? echo $class; ?></td>
									<td align="right"><? echo $cstats['total_da']; ?></td>
								</tr>
								<? // then sort by the total damage to/from other player
									$opsortda = array();
									foreach($cstats['players'] as $opname => $opstats) 
										$opsortda[$opname] = $opstats['total_da'];
									array_multisort($opsortda, SORT_DESC, $cstats['players']);

									// printing data
									foreach ($cstats['players'] as $opname => $opstats): ?>
									<tr class="op-name">
										<td class="indent1"><? echo $opstats['pdata']['pname'] ?></td>
										<td>
											
									<? // last and final sort based on damage to/from o. player's class
										$opcsortda = array();
										foreach($opstats['classes'] as $opclass => $opcstats) 
											$opcsortda[$opclass] = $opcstats['da'];
										array_multisort($opcsortda, SORT_DESC, $opstats['classes']);

										// printing data
										foreach ($opstats['classes'] as $opclass => $opcstats): ?>
											<table class="table noborder">
												<td><? echo $opclass; ?></td>
												<td align="right"><? echo $opcstats['da']; ?></td>
											</tr>
											</table>
									<?	endforeach; ?>
										</td>
									</tr>
									<?
								endforeach;
							endforeach;
						endif;
						?> </tbody></table> </div></div> <?
					endforeach;
					?> </div> <?
				endforeach;
			endif;
		endif;
	endif;
?>
			</div>
		</div>
	</div>
<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
</BODY>
</HTML>